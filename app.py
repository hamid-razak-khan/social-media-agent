import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from utils.formatter import build_filename, wrap_content_for_download

# Load environment variables from .env (OPENAI_API_KEY, OPENAI_MODEL_NAME, etc.)
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "prompts" / "content_prompt.txt"


@st.cache_resource(show_spinner=False)
def get_llm() -> ChatGroq:
    """Create a cached OpenAI chat model instance for LangChain."""
    model_name = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-20b")
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name=model_name,
        temperature=0.8,
    )


@st.cache_resource(show_spinner=False)
def get_prompt_template() -> PromptTemplate:
    template_str = PROMPT_PATH.read_text(encoding="utf-8")
    return PromptTemplate(
        input_variables=[
            "business_type",
            "target_audience",
            "tone",
            "platform",
            "content_type",
            "extra_instructions",
        ],
        template=template_str,
    )


def generate_content(
    business_type: str,
    target_audience: str,
    tone: str,
    platform: str,
    content_type: str,
    extra_instructions: str | None = None,
) -> str:
    """Generate social media content using LangChain + OpenAI.

    This function wires the PromptTemplate to the OpenAI chat model
    and returns plain text (Markdown) output.
    """

    llm = get_llm()
    prompt = get_prompt_template()
    chain = prompt | llm | StrOutputParser()

    inputs = {
        "business_type": business_type.strip(),
        "target_audience": target_audience.strip(),
        "tone": tone.lower().strip(),
        "platform": platform.strip(),
        "content_type": content_type.strip().lower(),
        "extra_instructions": (extra_instructions or "").strip() or "N/A",
    }

    return chain.invoke(inputs)


def _inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        /* Make the main container a bit wider and cleaner */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }

        /* Sidebar layout & border for a clean aligned look */
        section[data-testid="stSidebar"] {
            background-color: #020617;
            border-right: 1px solid rgba(148, 163, 184, 0.35);
        }

        section[data-testid="stSidebar"] > div {
            padding: 1.5rem 1.25rem 2rem;
        }

        /* Tighter spacing between sidebar widgets */
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.75rem;
        }

        /* Inputs in the sidebar share the same border and radius */
        section[data-testid="stSidebar"] .stTextInput > div > div,
        section[data-testid="stSidebar"] .stSelectbox > div > div,
        section[data-testid="stSidebar"] textarea {
            border-radius: 0.6rem;
            border: 1px solid rgba(148, 163, 184, 0.35);
        }

        /* Buttons */
        .stButton > button {
            border-radius: 999px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Social Media Content Agent",
        page_icon="✨",
        layout="wide",
    )

    _inject_custom_css()

    st.title("Social Media Content Generator Agent")
    st.caption(
        "Use AI to generate platform-optimized captions, ideas, hashtags, reels concepts, and weekly plans."
    )

    with st.sidebar:
        st.header("Content Settings")

        business_type = st.text_input(
            "Business type",
            placeholder="e.g. Online fitness coaching brand",
        )
        target_audience = st.text_input(
            "Target audience",
            placeholder="e.g. Busy professionals in their 30s",
        )

        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Inspirational", "Humorous"],
            index=0,
        )

        platform = st.selectbox(
            "Platform",
            ["Instagram", "LinkedIn", "Twitter", "YouTube"],
            index=0,
        )

        content_type_label_map = {
            "Caption": "caption",
            "Post ideas": "post ideas",
            "Hashtags": "hashtags",
            "Reels ideas": "reels ideas",
            "Weekly plan": "weekly plan",
        }

        content_type_label = st.selectbox(
            "Content type",
            list(content_type_label_map.keys()),
            index=0,
        )
        content_type_value = content_type_label_map[content_type_label]

        extra_instructions = st.text_area(
            "Additional instructions (optional)",
            placeholder=(
                "e.g. Focus on lead generation, highlight limited-time offer, "
                "avoid using discounts, write in UK English, etc."
            ),
            height=140,
        )

        st.divider()
        generate_btn = st.button("Generate content", type="primary", use_container_width=True)

    st.markdown("### Generated content")
    st.divider()

    if generate_btn:
        if not business_type or not target_audience:
            st.warning("Please fill in both business type and target audience.")
            return

        with st.spinner("Thinking and drafting your content..."):
            try:
                output_text = generate_content(
                    business_type=business_type,
                    target_audience=target_audience,
                    tone=tone,
                    platform=platform,
                    content_type=content_type_value,
                    extra_instructions=extra_instructions,
                )
            except Exception as exc:  # noqa: BLE001
                st.error(
                    "Failed to generate content. "
                    "Check your GROQ_API_KEY and network, then try again."
                )
                st.exception(exc)
                return

        st.success("Content generated successfully.")

        st.markdown(output_text)

        st.divider()

        meta = {
            "Business type": business_type,
            "Target audience": target_audience,
            "Tone": tone,
            "Platform": platform,
            "Content type": content_type_label,
        }

        download_text = wrap_content_for_download(output_text, meta)
        filename = build_filename(business_type, platform, content_type_label)

        st.download_button(
            label="Download as .txt",
            data=download_text,
            file_name=filename,
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
