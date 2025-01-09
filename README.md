# Self-Guided Learning App

This application demonstrates a simple, self-guided learning approach. It allows you to:
- Enter a topic
- Choose preferences (Learning Style, Audience Age, Content Length, Knowledge Level)
- Generate a specified number of subtopics (3, 5, or 10)
- View each generated item in a responsive three-panel layout

**Key Features**  
1. **Responsive Layout**  
   - **Top Panel**: Input fields, plus “Generate” button  
   - **Second Panel**: List of generated subtopics/items  
   - **Third Panel**: Displays the selected item’s content  
   - Adapts automatically to mobile (vertical stacking) or wider screens (horizontal arrangement).
2. **No Custom Code**  
   - The code in this repository was built entirely using **o1 pro** with iterative prompting, containing no manually authored code.
3. **Default Values**  
   - **Number of Items**: 3  
   - **Knowledge Level**: “Basic”  

**How to Use**  
1. **Install** dependencies with `requirements.txt`.  
2. **Set** your OpenAI key in `.env`.  
3. **Run** the application with `streamlit run main.py`.  
4. **Enter** a topic and choose preferences.  
5. **Click** “Generate” to produce subtopics and content.  
6. **Select** any item in the second panel to view it in the third panel.

---

## **2. `requirements.txt`**

```txt
streamlit==1.25.0
openai==0.27.0
python-dotenv==1.0.0