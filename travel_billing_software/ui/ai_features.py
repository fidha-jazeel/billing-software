# travel_billing_software/ui/ai_features_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

try:
    # Backend agent that talks to the billing.db
    from travel_billing_software.utils.sql_react_agent import get_agent_report
except ImportError:
    get_agent_report = None


class AIWorkerThread(QThread):
    """Background thread for AI processing to prevent UI freezing."""
    finished = pyqtSignal(str)  # Emits the result
    error = pyqtSignal(str)     # Emits error message
    
    def __init__(self, question: str):
        super().__init__()
        self.question = question
    
    def run(self):
        """Run AI processing in background."""
        try:
            if get_agent_report is None:
                self.error.emit("AI is not configured. Check sql_react_agent.py and GOOGLE_API_KEY.")
                return
            
            result = get_agent_report(self.question)
            
            # Parse result
            text = ""
            if isinstance(result, str):
                text = result
            elif isinstance(result, dict):
                if "output" in result:
                    text = result["output"]
                elif "answer" in result:
                    text = result["answer"]
                else:
                    text = str(result)
            else:
                text = str(result)
            
            self.finished.emit(text)
            
        except Exception as e:
            self.error.emit(f"AI Error: {str(e)}")


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
        
        self.worker_thread = None  # Track active AI thread

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
        btn_this_month.setCursor(Qt.CursorShape.PointingHandCursor)

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
        btn_last_vs_this.setCursor(Qt.CursorShape.PointingHandCursor)

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
        btn_top_customers.setCursor(Qt.CursorShape.PointingHandCursor)

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
        btn_pending.setCursor(Qt.CursorShape.PointingHandCursor)

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
        self.ask_button.setCursor(Qt.CursorShape.PointingHandCursor)

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
        """Call the SQL + LLM agent in background thread."""
        if get_agent_report is None:
            QMessageBox.critical(
                self,
                "AI Not Available",
                "AI is not configured.\n\n"
                "Please check sql_react_agent.py and your GOOGLE_API_KEY.",
            )
            return
        
        # Prevent multiple simultaneous requests
        if self.worker_thread and self.worker_thread.isRunning():
            QMessageBox.information(
                self,
                "AI Busy",
                "AI is still processing your previous question.\nPlease wait..."
            )
            return

        try:
            # Show loading state
            self.answer_box.setPlainText("🤖 AI is thinking...\n\nPlease wait, this may take 10-15 seconds.\nYou can continue using other parts of the software.")
            self.ask_button.setEnabled(False)
            self.ask_button.setText("Processing...")
            
            # Create and start worker thread
            self.worker_thread = AIWorkerThread(question)
            self.worker_thread.finished.connect(self._on_ai_success)
            self.worker_thread.error.connect(self._on_ai_error)
            self.worker_thread.start()

        except Exception as e:
            self._on_ai_error(f"Failed to start AI: {str(e)}")
    
    def _on_ai_success(self, result: str):
        """Handle successful AI response."""
        self.answer_box.setPlainText(result)
        self.ask_button.setEnabled(True)
        self.ask_button.setText("Ask AI")
    
    def _on_ai_error(self, error_msg: str):
        """Handle AI error."""
        self.answer_box.setPlainText(
            f"❌ Error:\n\n{error_msg}\n\n"
            "Please try again or contact support if the issue persists."
        )
        self.ask_button.setEnabled(True)
        self.ask_button.setText("Ask AI")
