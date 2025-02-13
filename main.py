import streamlit as st
import io
from merger_tools import *


with st.form('form', clear_on_submit=True, border=False):
    upload_files = st.file_uploader(label="Upload your files", type=['png', 'jpg', 'jpeg', 'pdf'],
                                    accept_multiple_files=True)
    status = st.form_submit_button(label="Объединить файлы")

if upload_files is not None and status:
    files = [(io.BytesIO(item.getvalue()), item.name.split('.')[-1]) for item in upload_files]
    upload_files.clear()
    try:
        data = merge(files)
        st.download_button("Скачать объединенные файлы", data, file_name="merged_files.pdf", mime="application/pdf")
    except Exception:
        st.write('<h2>Во время обработки возникли ошибки, возможно один из файлов поврежден :(</h2>',
                 unsafe_allow_html=True)



