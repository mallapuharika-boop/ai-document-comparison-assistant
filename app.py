
import streamlit as st

from document_reader import extract_text_from_pdf
from comparison import compare_documents
from report_generator import generate_comparison_report


st.set_page_config(
    page_title="AI Document Comparison Assistant",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Document Comparison Assistant")

st.write(
    "Upload two PDF documents to identify similarities, differences, "
    "key details, and important changes."
)

st.info(
    "This tool provides AI-generated analysis. "
    "Please verify important findings against the original documents."
)

# Upload two documents
col1, col2 = st.columns(2)

with col1:
    st.subheader("Document A")
    file_a = st.file_uploader(
        "Upload the first PDF",
        type=["pdf"],
        key="document_a",
    )

with col2:
    st.subheader("Document B")
    file_b = st.file_uploader(
        "Upload the second PDF",
        type=["pdf"],
        key="document_b",
    )

# Preview uploaded documents
if file_a is not None:
    st.success(f"Document A: {file_a.name}")

if file_b is not None:
    st.success(f"Document B: {file_b.name}")

# Compare button
if st.button("🔍 Compare Documents", type="primary"):
    if file_a is None or file_b is None:
        st.error("Please upload both PDF documents first.")

    elif file_a.getvalue() == file_b.getvalue():
        st.warning(
            "Both uploaded files have identical contents. "
            "Please upload two different documents."
        )

    else:
        try:
            with st.spinner(
                "Reading PDFs and comparing documents with Gemini AI..."
            ):
                document_a = extract_text_from_pdf(file_a)
                document_b = extract_text_from_pdf(file_b)

                comparison = compare_documents(
                    document_a,
                    document_b,
                )

                report_bytes = generate_comparison_report(
                    document_a,
                    document_b,
                    comparison,
                )

                st.session_state["comparison_result"] = comparison
                st.session_state["report_bytes"] = report_bytes
                st.session_state["document_a_name"] = document_a["filename"]
                st.session_state["document_b_name"] = document_b["filename"]

        except Exception as error:
            st.error(str(error))

# Display results saved in the session
if "comparison_result" in st.session_state:
    result = st.session_state["comparison_result"]

    st.divider()
    st.header("📊 Comparison Results")

    tab_a, tab_b, tab_sim, tab_diff, tab_details, tab_final = st.tabs(
        [
            "Document A",
            "Document B",
            "Similarities",
            "Differences",
            "Key Details",
            "Conclusion",
        ]
    )

    with tab_a:
        st.subheader(st.session_state["document_a_name"])
        st.write(result["document_a_summary"])

    with tab_b:
        st.subheader(st.session_state["document_b_name"])
        st.write(result["document_b_summary"])

    with tab_sim:
        st.subheader("Similarities")

        if result["similarities"]:
            for item in result["similarities"]:
                st.markdown(f"- {item}")
        else:
            st.write("No supported similarities were identified.")

    with tab_diff:
        st.subheader("Differences")

        if result["differences"]:
            for index, item in enumerate(result["differences"], start=1):
                with st.expander(
                    f"{index}. {item.get('topic', 'Difference')}"
                ):
                    st.write(
                        f"**Change type:** "
                        f"{item.get('change_type', 'Not specified')}"
                    )
                    st.write(
                        f"**Document A:** "
                        f"{item.get('document_a', 'Not found')}"
                    )
                    st.write(
                        f"**Document B:** "
                        f"{item.get('document_b', 'Not found')}"
                    )
                    st.write(
                        f"**Evidence:** "
                        f"{item.get('evidence', 'Not provided')}"
                    )
        else:
            st.write("No supported differences were identified.")

    with tab_details:
        st.subheader("Key Details")

        if result["key_details"]:
            st.dataframe(
                result["key_details"],
                use_container_width=True,
            )
        else:
            st.write("No key details were returned.")

    with tab_final:
        st.subheader("Overall Conclusion")
        st.write(result["overall_conclusion"])

        st.subheader("Limitations")

        if result["limitations"]:
            for item in result["limitations"]:
                st.markdown(f"- {item}")
        else:
            st.write("No additional limitations were reported.")

    st.divider()
    st.subheader("📥 Download Comparison Report")

    st.download_button(
        label="Download Report (.docx)",
        data=st.session_state["report_bytes"],
        file_name="document_comparison_report.docx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    )

    if st.button("🔄 Start a New Comparison"):
        for key in [
            "comparison_result",
            "report_bytes",
            "document_a_name",
            "document_b_name",
        ]:
            st.session_state.pop(key, None)

        st.rerun()
