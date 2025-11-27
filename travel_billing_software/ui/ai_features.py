# travel_billing_software/ui/ai_features_page.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt

try:
    # Backend agent that talks to the billing.db
    from travel_billing_software.utils.sql_react_agent import get_agent_report
except ImportError:
    get_agent_report = None


class AIFeaturesPage(QWidget):
    """
    Simple AI Insights page for small travel agency.
    Shows easy-to-understand summaries using the SQL + LLM agent.
    """

    def __init__(
        self,
        colors,
        app_config,
        get_button_style,
        get_input_style,
        get_label_style,
        get_scrollarea_style,
        parent=None,
    ):
        super().__init__(parent)
        self.COLORS = colors
        self.APP_CONFIG = app_config
        self.get_button_style = get_button_style
        self.get_input_style = get_input_style
        self.get_label_style = get_label_style
        self.get_scrollarea_style = get_scrollarea_style

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area like other pages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self.get_scrollarea_style())

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        heading = QLabel("🤖 AI Insights")
        heading.setStyleSheet(
            f"color: {self.COLORS['accent_secondary']}; font-size: 25px; font-weight: bold;"
        )
        layout.addWidget(heading)

        sub = QLabel(
            "Ask simple questions like:\n"
            "• \"How much did we earn this month?\"\n"
            "• \"How many invoices are pending?\"\n"
            "• \"Who are my top customers this month?\""
        )
        sub.setStyleSheet(
            f"color: {self.COLORS['text_secondary']}; font-size: 20px;"
        )
        sub.setWordWrap(True)
        layout.addWidget(sub)

        # === PRESET QUESTIONS SECTION ===
        presets_frame = QFrame()
        presets_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.COLORS['secondary_bg']};
                border-radius: 8px;
                padding: 10px 12px;
            }}
        """
        )
        presets_layout = QVBoxLayout(presets_frame)
        presets_layout.setSpacing(8)

        presets_title = QLabel("⭐ Quick AI Insights")
        presets_title.setStyleSheet(
            f"color: {self.COLORS['accent_primary']}; font-weight: bold;font-size:20px;"
        )
        presets_layout.addWidget(presets_title)

        row1 = QHBoxLayout()
        row1.setSpacing(8)

        btn_this_month = QPushButton("📅 This Month Overview")
        btn_this_month.setStyleSheet(self.get_button_style("add"))
        btn_this_month.setCursor(Qt.PointingHandCursor)
        btn_this_month.clicked.connect(
            lambda: self.ask_ai(
                "Give a very simple summary for this month for my travel agency. "
                "Include: total revenue, number of invoices, and how many are pending. "
                "Explain in very easy language, 4-5 bullet points only."
            )
        )
        row1.addWidget(btn_this_month)

        btn_last_vs_this = QPushButton("📈 This vs Last Month")
        btn_last_vs_this.setStyleSheet(self.get_button_style("add"))
        btn_last_vs_this.setCursor(Qt.PointingHandCursor)
        btn_last_vs_this.clicked.connect(
            lambda: self.ask_ai(
                "Compare this month and last month for my billing data. "
                "Explain: did revenue go up or down, how many invoices, and pending amounts. "
                "Use very simple language and short bullet points."
            )
        )
        row1.addWidget(btn_last_vs_this)

        presets_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(8)

        btn_top_customers = QPushButton("👥 Top Customers")
        btn_top_customers.setStyleSheet(self.get_button_style("add"))
        btn_top_customers.setCursor(Qt.PointingHandCursor)
        btn_top_customers.clicked.connect(
            lambda: self.ask_ai(
                "Show my top 5 customers by total billing amount. "
                "Show a small table with customer name and total amount. "
                "Then give 2-3 simple lines explaining what you see."
            )
        )
        row2.addWidget(btn_top_customers)

        btn_pending = QPushButton("⏳ Pending Payments")
        btn_pending.setStyleSheet(self.get_button_style("add"))
        btn_pending.setCursor(Qt.PointingHandCursor)
        btn_pending.clicked.connect(
            lambda: self.ask_ai(
                "Summarise my pending invoices. "
                "Tell total pending amount, number of pending invoices, "
                "and if there are any very old pending invoices. "
                "Explain simply in bullet points."
            )
        )
        row2.addWidget(btn_pending)

        presets_layout.addLayout(row2)

        layout.addWidget(presets_frame)

        # === CUSTOM QUESTION SECTION ===
        custom_frame = QFrame()
        custom_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.COLORS['secondary_bg']};
                border-radius: 8px;
                padding: 15px;
            }}
        """
        )
        custom_layout = QVBoxLayout(custom_frame)
        custom_layout.setSpacing(10)

        custom_label = QLabel("✍️ Ask your own question")
        custom_label.setStyleSheet(
            f"color: {self.COLORS['accent_cyan']}; font-weight: bold;font-size:20px;"
        )
        custom_layout.addWidget(custom_label)

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText(
            "Example: \"How many visa-only invoices did we create this month?\""
        )
        self.question_input.setStyleSheet(self.get_input_style())
        custom_layout.addWidget(self.question_input)

        ask_row = QHBoxLayout()
        ask_row.addStretch()
        self.ask_button = QPushButton("Ask AI")
        self.ask_button.setStyleSheet(self.get_button_style("save"))
        self.ask_button.setCursor(Qt.PointingHandCursor)
        self.ask_button.clicked.connect(self.on_custom_ask)
        ask_row.addWidget(self.ask_button)
        custom_layout.addLayout(ask_row)

        # === ANSWER AREA ===
        answer_label = QLabel("📄 AI Answer")
        answer_label.setStyleSheet(self.get_label_style(bold=True))
        custom_layout.addWidget(answer_label)

        self.answer_box = QTextEdit()
        self.answer_box.setReadOnly(True)
        self.answer_box.setStyleSheet(
            f"""
            QTextEdit {{
                background-color: {self.COLORS['primary_bg']};
                color: {self.COLORS['text_primary']};
                border-radius: 5px;
                border: 1px solid #444;
                padding: 8px;
                font-size: 12px;
            }}
        """
        )
        custom_layout.addWidget(self.answer_box)

        layout.addWidget(custom_frame)

        layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # If agent not available, show a friendly warning once
        if get_agent_report is None:
            self.answer_box.setPlainText(
                "AI is not configured yet.\n\n"
                "Please make sure 'sql_react_agent.py' is available and "
                "GOOGLE_API_KEY is set in your environment."
            )

    # ---------- Logic ----------

    def on_custom_ask(self):
        question = self.question_input.text().strip()
        if not question:
            QMessageBox.warning(self, "Empty Question", "Please type a question first.")
            return
        self.ask_ai(
            question
            + "\n\nPlease answer in very simple English, "
            "with short bullet points suitable for a small travel agency."
        )

    def ask_ai(self, question: str):
        """Call the SQL + LLM agent and display result."""
        if get_agent_report is None:
            QMessageBox.critical(
                self,
                "AI Not Available",
                "AI is not configured.\n\n"
                "Please check sql_react_agent.py and your GOOGLE_API_KEY.",
            )
            return

        try:
            self.answer_box.setPlainText("Thinking...\nPlease wait a moment.")
            self.ask_button.setEnabled(False)

            result = get_agent_report(question)

            # LangChain agents may return different shapes. Handle a few common ones.
            text = ""
            if isinstance(result, str):
                text = result
            elif isinstance(result, dict):
                # Try typical keys
                if "output" in result:
                    text = result["output"]
                elif "answer" in result:
                    text = result["answer"]
                else:
                    text = str(result)
            else:
                text = str(result)

            self.answer_box.setPlainText(text)

        except Exception as e:
            self.answer_box.setPlainText(
                "Sorry, I could not generate insights.\n\n"
                f"Technical error: {e}"
            )
            QMessageBox.critical(
                self,
                "AI Error",
                f"Something went wrong while calling the AI:\n{e}",
            )
        finally:
            self.ask_button.setEnabled(True)
