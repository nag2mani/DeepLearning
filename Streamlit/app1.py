import streamlit as st


# Title
st.title("Pdf Reader")


# Header and Subheader
st.header("header")
st.subheader("Subheader")


# text
st.text("Hello")


# markdown
st.markdown(" # This is our first markdown")
st.markdown(" ## This is our first markdown")
st.markdown(" ### This is our first markdown")
st.markdown(" #### This is our first markdown")


# Text color
st.success("Scuessful Done")
st.info("Information")
st.warning("This is a warning")
st.error("This is an error")


# Exception
st.exception("NameError('name pd is not defiened')")


#Help
import pandas
st.help(pandas)
st.help(range)


# Writing text
st.write("Text with write")
st.write(range(10))