# app.py
import streamlit as st
import openai
from datetime import datetime
import pandas as pd
import json
import re

from openai import OpenAI
st.write("Secrets:", st.secrets)

apikey = st.secrets["apikey"]
openai.api_key = apikey

# --- App Title ---
st.title("💸 Spending Info Extractor")

# --- User Input Section ---
st.write("### Enter your spending descriptions (one per line)")
input_text = st.text_area("Type each expense line by line", height=200, placeholder="e.g.\nphở 50k\ntrà sữa 35k\n...")

if st.button("Extract Spending Info"):
    
    # --- Process Input ---
    inputs = [line.strip() for line in input_text.strip().split("\n") if line.strip()]
    df = pd.DataFrame()

    client = openai.OpenAI(api_key=apikey)

    for i in inputs:
        prompt = f"""You are a finance assistant. Extract spending info from this sentence. If there are any typos, fix them.
Return a JSON output with the following keys: date, item, amount, category. Assume today is {datetime.today().date()}.
Input: {i}
IMPORTANT: only return the JSON without any other text.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content
            cleaned = re.sub(r"```json|```", "", result, flags=re.IGNORECASE).strip()
            data = json.loads(cleaned)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        except Exception as e:
            st.error(f"Failed to process input: '{i}'\nError: {e}")

    # --- Show Result ---
    st.success("✅ Extraction completed!")
    st.dataframe(df)

# if __name__ == "__main__":
#     main()
