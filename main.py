"""
main.py

Responsive 3-panel layout:
- Top panel (inputs) spans full width.
- Second panel (generated items) + third panel (content).
- For small widths (<768px), second/third stack vertically.
- For moderate widths (>=768px), second/third side by side.
- For very wide screens (>1200px), center the container and let second panel have a smaller fixed width, 
  third panel fills the rest, mimicking a "center=8, right=2" style.
"""

import streamlit as st
import uuid
from openai_api import generate_subtopics, generate_content
from prompt_utils import build_subtopics_prompt, build_content_prompt

# Setup wide layout
st.set_page_config(page_title="Self-Guided Learning App", layout="wide")

# Session state
if "generated_items" not in st.session_state:
    st.session_state.generated_items = []
if "selected_item_id" not in st.session_state:
    st.session_state.selected_item_id = None

def add_item(subtopic, style_val, length_val, knowledge_val, content):
    new_id = str(uuid.uuid4())
    item = {
        "id": new_id,
        "subtopic": subtopic,
        "style": style_val,
        "length": length_val,
        "knowledge_level": knowledge_val,
        "content": content
    }
    st.session_state.generated_items.append(item)
    st.session_state.selected_item_id = new_id

# Inject custom CSS for the responsive 3-panel layout
st.markdown(
    """
    <style>
    /* The main container for all panels */
    .app-container {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-top: 1rem;
      margin-left: auto;
      margin-right: auto;
      /* We'll let a media query handle max-width for large screens */
    }

    /* Top panel always 100% width */
    .top-panel {
      background: #fff;
      flex: 1 1 100%;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      border-radius: 8px;
      padding: 1rem;
    }

    /* By default, second & third panels share space horizontally, 
       but can stack on small screens using media queries. */
    .second-panel {
      background: #fff;
      flex: 1 1 300px; 
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      border-radius: 8px;
      padding: 1rem;
    }
    .third-panel {
      background: #fff;
      flex: 2 1 600px; 
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      border-radius: 8px;
      padding: 1rem;
    }

    /* For small screens: stack second & third vertically */
    @media (max-width: 768px) {
      .second-panel, .third-panel {
        flex: 1 1 100%;
      }
    }

    /* For large screens: center the container + 
       give second panel a narrower fixed width 
       so it looks like "8,2" ratio. 
       Or tweak to your desired ratio. 
    */
    @media (min-width: 1200px) {
      .app-container {
        max-width: 1200px; 
      }
      .second-panel {
        flex: 0 0 250px; /* fixed ~2 columns */
        max-width: 250px;
      }
      .third-panel {
        flex: 1 1 auto; 
      }
    }

    /* Style for the selected item */
    .selected-item-button {
      background-color: #cceeff;
      border: 2px solid red;
      color: #003366;
      padding: 0.6rem;
      margin-bottom: 0.5rem;
      border-radius: 4px;
      font-weight: 600;
      width: 100%;
      text-align: left;
    }
    /* unselected items are normal st.buttons, no extra styling needed */
    </style>
    """,
    unsafe_allow_html=True
)

# Layout: we won't use st.columns, but raw HTML containers
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# ------------- TOP PANEL (Inputs) -------------
st.markdown('<div class="top-panel">', unsafe_allow_html=True)
st.markdown("## Self-Guided Learning App")
st.markdown("Enter a topic and choose your preferences. Then click **Generate** to create subtopics & content.")

# We'll build the input fields using columns
c1, c2, c3, c4 = st.columns(4)

with c1:
    topic = st.text_input("Topic", value="Probability and Statistics")

with c2:
    style = st.selectbox(
        "Learning Style",
        ["Storytelling", "Expository", "Interactive Examples", "Analogies & Metaphors", "Practice-based"]
    )

with c3:
    age = st.selectbox(
        "Target Audience Age",
        ["Child (6-10)", "Preteen (11-13)", "Teen (14-17)", "Young Adult (18-25)", "Adult (26+)"]
    )

with c4:
    length = st.selectbox("Content Length", ["Short", "Medium", "Long"])

c5, c6 = st.columns([3,1])
with c5:
    knowledge_options = ["None", "Basic", "Intermediate", "Advanced"]
    knowledge_level = st.selectbox("Knowledge Level", knowledge_options, index=1)

with c6:
    num_options = [3,5,10]
    num_to_generate = st.radio("Items to Generate", num_options, index=0, horizontal=True)

    if st.button("Generate"):
        if not topic.strip():
            st.warning("Please enter a valid topic.")
        else:
            with st.spinner("Generating subtopics..."):
                subtopic_prompt = build_subtopics_prompt(topic)
                all_subtopics = generate_subtopics(subtopic_prompt)

            if not all_subtopics:
                st.error("No subtopics returned. Please try again.")
            else:
                selected_subtopics = all_subtopics[:num_to_generate]
                total = len(selected_subtopics)
                prog_bar = st.progress(0)

                for i, sub in enumerate(selected_subtopics, start=1):
                    with st.spinner(f"Generating content for {sub}..."):
                        c_prompt = build_content_prompt(topic, sub, style, age, length, knowledge_level)
                        c_text = generate_content(c_prompt)
                    add_item(sub, style, length, knowledge_level, c_text)
                    prog_bar.progress(int((i / total) * 100))

                st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)  # End top-panel

# ------------- SECOND PANEL (Generated Items) -------------
st.markdown('<div class="second-panel">', unsafe_allow_html=True)
st.markdown("### Generated Items")
if not st.session_state.generated_items:
    st.write("No items yet.")
else:
    for itm in reversed(st.session_state.generated_items):
        list_id = itm["id"]
        display_name = itm["subtopic"]

        if st.session_state.selected_item_id == list_id:
            # selected => light blue background + red border
            st.markdown(f'<div class="selected-item-button">{display_name}</div>', unsafe_allow_html=True)
        else:
            if st.button(display_name, key=f"select_{list_id}"):
                st.session_state.selected_item_id = list_id
                st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)  # End second-panel

# ------------- THIRD PANEL (Selected Content) -------------
st.markdown('<div class="third-panel">', unsafe_allow_html=True)
selected_item = None
for itm in st.session_state.generated_items:
    if itm["id"] == st.session_state.selected_item_id:
        selected_item = itm
        break

if selected_item:
    st.subheader(selected_item["subtopic"])
    st.write(selected_item["content"])
else:
    st.info("Select an item in the second panel to view its content here.")

st.markdown('</div>', unsafe_allow_html=True)  # End third-panel

st.markdown('</div>', unsafe_allow_html=True)  # End app-container