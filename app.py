import bibtexparser
import streamlit as st

st.title("Abbreviate Journal Names in BibTeX")

@st.cache_data
def load_abbreviations():
    with open("All_abbrev.txt", "r") as f:
        abbrev_list = f.read().splitlines()
    abbreviations = {}
    for line in abbrev_list:
        value, key = line.split("\t")
        abbreviations[key] = value
    return abbreviations

uploaded_file = st.file_uploader("Upload a BibTeX file", type="bib" )
abbreviations = load_abbreviations()
if uploaded_file is not None:
    bib_database  = bibtexparser.parse_string(uploaded_file.getvalue().decode())

    with st.spinner("Generating abbreviations"):
        for entry in bib_database.entries:
            if "journal" in entry:
                journal = entry["journal"]
                if journal in abbreviations:
                    entry["journal"] = abbreviations[journal]

    bib_database_str = bibtexparser.write_string(bib_database)
    st.download_button("Download updated references", bib_database_str, "abbreviated.bib", type="primary")

    # First 10 entries
    st.write("First 10 entries:")
    block = bib_database.blocks[:10]
    first_entry_lib = bibtexparser.Library(blocks=[block])
    first_entry_str = bibtexparser.write_string(first_entry_lib)
    st.code(first_entry_str, language="latex")
