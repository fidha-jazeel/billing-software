"""
Reports Page Module
Contains invoice history, analytics dashboard, and invoice management functions.
"""
import os
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QFileDialog, QHeaderView)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor


class ReportsPage(QWidget):
    """Reports page with invoice history and analytics."""
    
    def __init__(self, colors, invoice_config, app_config, get_table_style, get_button_style,
                 get_input_style, get_label_style, dashboard_ref):
        """
        Initialize Reports page.
        
        Args:
            colors: Color scheme dictionary
            invoice_config: Invoice configuration dictionary
            app_config: Application configuration
            get_table_style: Function to get table stylesheet
            get_button_style: Function to get button stylesheet
            get_input_style: Function to get input stylesheet
            get_label_style: Function to get label stylesheet
            dashboard_ref: Reference to parent dashboard for accessing widgets
        """
        super().__init__()
        self.colors = colors
        self.invoice_config = invoice_config
        self.app_config = app_config
        self.get_table_style = get_table_style
        self.get_button_style = get_button_style
        self.get_input_style = get_input_style
        self.get_label_style = get_label_style
        self.dashboard = dashboard_ref
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {self.colors['primary_bg']};
            }}
        """)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        heading = QLabel(f"<h2 style='color:{self.colors['accent_secondary']};'>📊 Reports & Analytics</h2>")
        layout.addWidget(heading)
        
        # Analytics Section
        analytics_frame = self._create_analytics_frame()
        layout.addWidget(analytics_frame)
        
        # Invoice History Section
        invoices_heading = QLabel(f"<h3 style='color:{self.colors['accent_cyan']};'>📄 Invoice History</h3>")
        layout.addWidget(invoices_heading)

        # Search and refresh
        search_layout = QHBoxLayout()
        
        search_label = QLabel("Search:")
        search_label.setStyleSheet(self.get_label_style(bold=True))
        search_layout.addWidget(search_label)
        
        self.search_invoice = QLineEdit()
        self.search_invoice.setPlaceholderText("Search by invoice number, customer name...")
        self.search_invoice.setStyleSheet(self.get_input_style())
        self.search_invoice.textChanged.connect(self.filter_invoices)
        search_layout.addWidget(self.search_invoice)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style('add'))
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        refresh_btn.clicked.connect(self.refresh_reports)
        search_layout.addWidget(refresh_btn)
        
        layout.addLayout(search_layout)

        # Invoice list table
        self.invoice_table = QTableWidget(0, 6)
        self.invoice_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Total", "Status", "Actions"
        ])
        
        # Set column widths
        header = self.invoice_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.resizeSection(5, 280)
        
        self.invoice_table.setStyleSheet(self.get_table_style())
        self.invoice_table.setMinimumHeight(400)
        layout.addWidget(self.invoice_table)

        # Load invoices
        self.load_invoices()

        layout.addStretch()
        
        scroll.setWidget(content)
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
    
    def _create_analytics_frame(self) -> QFrame:
        """Create analytics dashboard frame."""
        analytics_frame = QFrame()
        analytics_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        analytics_layout = QVBoxLayout(analytics_frame)
        analytics_layout.setSpacing(20)
        
        # Analytics title
        analytics_title = QLabel(f"<b style='color:{self.colors['accent_primary']}; font-size:16px;'>📈 Business Analytics</b>")
        analytics_layout.addWidget(analytics_title)
        
        # Calculate analytics
        self.analytics_data = self.calculate_analytics()
        
        # Create metric cards
        self.metric_cards = {}
        
        # Row 1: Financial Metrics
        financial_row = QHBoxLayout()
        financial_row.setSpacing(15)
        
        revenue_card = self.create_metric_card("💰 Total Revenue", 
                                               f"₹{self.analytics_data['total_revenue']:,.2f}")
        financial_row.addWidget(revenue_card)
        self.metric_cards['revenue'] = revenue_card
        
        received_card = self.create_metric_card("✅ Received Amount", 
                                                f"₹{self.analytics_data['received_amount']:,.2f}")
        financial_row.addWidget(received_card)
        self.metric_cards['received'] = received_card
        
        pending_card = self.create_metric_card("⏳ Pending Amount", 
                                               f"₹{self.analytics_data['pending_amount']:,.2f}")
        financial_row.addWidget(pending_card)
        self.metric_cards['pending'] = pending_card
        
        analytics_layout.addLayout(financial_row)
        
        # Row 2: Invoice Statistics
        stats_row = QHBoxLayout()
        stats_row.setSpacing(15)
        
        invoices_card = self.create_metric_card("📄 Total Invoices", 
                                                str(self.analytics_data['total_invoices']))
        stats_row.addWidget(invoices_card)
        self.metric_cards['invoices'] = invoices_card
        
        paid_card = self.create_metric_card("✅ Paid Invoices", 
                                           str(self.analytics_data['paid_count']))
        stats_row.addWidget(paid_card)
        self.metric_cards['paid'] = paid_card
        
        pending_inv_card = self.create_metric_card("⏳ Pending Invoices", 
                                                   str(self.analytics_data['pending_count']))
        stats_row.addWidget(pending_inv_card)
        self.metric_cards['pending_inv'] = pending_inv_card
        
        analytics_layout.addLayout(stats_row)
        
        # Row 3: Additional Analytics
        additional_row = QHBoxLayout()
        additional_row.setSpacing(15)
        
        avg_invoice_card = self.create_metric_card("📊 Avg Invoice Value", 
                                                   f"₹{self.analytics_data['avg_invoice']:,.2f}")
        additional_row.addWidget(avg_invoice_card)
        self.metric_cards['avg_invoice'] = avg_invoice_card
        
        customers_card = self.create_metric_card("👥 Total Customers", 
                                                str(self.analytics_data['total_customers']))
        additional_row.addWidget(customers_card)
        self.metric_cards['customers'] = customers_card
        
        collection_rate_card = self.create_metric_card("📈 Collection Rate", 
                                                       f"{self.analytics_data['collection_rate']:.1f}%")
        additional_row.addWidget(collection_rate_card)
        self.metric_cards['collection_rate'] = collection_rate_card
        
        analytics_layout.addLayout(additional_row)
        
        return analytics_frame
    
    def create_metric_card(self, title: str, value: str) -> QFrame:
        """Create a metric card widget."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary_bg']};
                border-radius: 6px;
                padding: 18px;
                min-width: 200px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(self.get_label_style(bold=True, size='small', color='text_secondary'))
        card_layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setProperty('metric_value', True)
        value_label.setStyleSheet(self.get_label_style(bold=True, size='title', color='accent_primary'))
        card_layout.addWidget(value_label)
        
        return card
    
    def calculate_analytics(self) -> dict:
        """Calculate analytics from invoice files."""
        analytics = {
            'total_revenue': 0.0,
            'total_invoices': 0,
            'pending_amount': 0.0,
            'received_amount': 0.0,
            'paid_count': 0,
            'pending_count': 0,
            'overpaid_count': 0,
            'avg_invoice': 0.0,
            'total_customers': 0,
            'collection_rate': 0.0
        }
        
        try:
            invoices_dir = self.invoice_config.get('save_directory', 'invoices')
            if not os.path.exists(invoices_dir):
                return analytics
            
            invoice_files = [f for f in os.listdir(invoices_dir) if f.endswith('.json')]
            analytics['total_invoices'] = len(invoice_files)
            
            customers_set = set()
            
            for filename in invoice_files:
                filepath = os.path.join(invoices_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Track unique customers
                    customer_name = data.get('customer_name', '').strip()
                    if customer_name:
                        customers_set.add(customer_name.lower())
                    
                    # Parse total
                    total_str = str(data.get('total', '₹0.00')).replace('₹', '').replace(',', '').strip()
                    try:
                        total = float(total_str)
                    except:
                        total = 0.0
                    analytics['total_revenue'] += total
                    
                    # Parse received
                    received_str = str(data.get('received', '0.00')).replace('₹', '').replace(',', '').strip()
                    try:
                        received = float(received_str)
                    except:
                        received = 0.0
                    analytics['received_amount'] += received
                    
                    # Parse balance
                    balance_str = str(data.get('balance', '₹0.00'))
                    
                    if 'Paid' in balance_str or '₹0.00' in balance_str or balance_str == '0.00':
                        analytics['paid_count'] += 1
                    elif 'Overpaid' in balance_str:
                        analytics['overpaid_count'] += 1
                    else:
                        analytics['pending_count'] += 1
                        pending_str = balance_str.replace('₹', '').replace(',', '').strip()
                        try:
                            pending = float(pending_str)
                            analytics['pending_amount'] += pending
                        except:
                            pass
                    
                except Exception as e:
                    print(f"Error processing invoice {filename}: {e}")
            
            # Calculate derived metrics
            analytics['total_customers'] = len(customers_set)
            
            if analytics['total_invoices'] > 0:
                analytics['avg_invoice'] = analytics['total_revenue'] / analytics['total_invoices']
            
            if analytics['total_revenue'] > 0:
                analytics['collection_rate'] = (analytics['received_amount'] / analytics['total_revenue']) * 100
                    
        except Exception as e:
            print(f"Error calculating analytics: {e}")
        
        return analytics
    
    def refresh_reports(self):
        """Refresh reports - reload invoices and update analytics."""
        print("🔄 Refreshing reports...")
        self.load_invoices()
        
        # Recalculate analytics
        self.analytics_data = self.calculate_analytics()
        
        # Update metric cards
        if hasattr(self, 'metric_cards'):
            updates = {
                'revenue': f"₹{self.analytics_data['total_revenue']:,.2f}",
                'received': f"₹{self.analytics_data['received_amount']:,.2f}",
                'pending': f"₹{self.analytics_data['pending_amount']:,.2f}",
                'invoices': str(self.analytics_data['total_invoices']),
                'paid': str(self.analytics_data['paid_count']),
                'pending_inv': str(self.analytics_data['pending_count']),
                'avg_invoice': f"₹{self.analytics_data['avg_invoice']:,.2f}",
                'customers': str(self.analytics_data['total_customers']),
                'collection_rate': f"{self.analytics_data['collection_rate']:.1f}%"
            }
            
            for card_name, new_value in updates.items():
                card = self.metric_cards.get(card_name)
                if card:
                    for child in card.findChildren(QLabel):
                        if child.property('metric_value'):
                            child.setText(new_value)
                            break
        
        print("✓ Reports refreshed successfully")
    
    def load_invoices(self):
        """Load all saved invoices."""
        try:
            self.invoice_table.setRowCount(0)
            
            invoices_dir = self.invoice_config.get('save_directory', 'invoices')
            if not os.path.exists(invoices_dir):
                print("⚠️ Invoices directory does not exist")
                return
            
            invoice_files = [f for f in os.listdir(invoices_dir) if f.endswith('.json')]
            invoice_files.sort(reverse=True)
            
            print(f"📄 Loading {len(invoice_files)} invoices...")
            
            for filename in invoice_files:
                filepath = os.path.join(invoices_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    row = self.invoice_table.rowCount()
                    self.invoice_table.insertRow(row)
                    
                    # Invoice Number
                    inv_num_item = QTableWidgetItem(data.get('invoice_number', 'N/A'))
                    inv_num_item.setForeground(QColor(self.colors['text_primary']))
                    self.invoice_table.setItem(row, 0, inv_num_item)
                    
                    # Date
                    date_item = QTableWidgetItem(data.get('invoice_date', 'N/A'))
                    date_item.setForeground(QColor(self.colors['text_secondary']))
                    self.invoice_table.setItem(row, 1, date_item)
                    
                    # Customer
                    customer_item = QTableWidgetItem(data.get('customer_name', 'N/A'))
                    customer_item.setForeground(QColor(self.colors['text_primary']))
                    self.invoice_table.setItem(row, 2, customer_item)
                    
                    # Total
                    total_value = data.get('total', '₹0.00')
                    total_item = QTableWidgetItem(str(total_value))
                    total_item.setForeground(QColor(self.colors['accent_gold']))
                    self.invoice_table.setItem(row, 3, total_item)
                    
                    # Status
                    balance_value = data.get('balance', '₹0.00')
                    balance_text = str(balance_value)
                    if 'Paid' in balance_text or balance_text == '₹0.00' or balance_value == 0:
                        status = '✅ Paid'
                        color = self.colors['success']
                    elif 'Overpaid' in balance_text:
                        status = '💰 Overpaid'
                        color = self.colors['info']
                    else:
                        status = '⏳ Pending'
                        color = self.colors['danger']
                    
                    status_item = QTableWidgetItem(status)
                    status_item.setForeground(QColor(color))
                    self.invoice_table.setItem(row, 4, status_item)
                    
                    # Actions buttons
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(5, 2, 5, 2)
                    actions_layout.setSpacing(5)
                    
                    # Edit button
                    edit_btn = QPushButton("✏️ Edit")
                    edit_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #7c3aed;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            padding: 6px 12px;
                            font-weight: bold;
                            font-size: 12px;
                            min-width: 70px;
                        }
                        QPushButton:hover {
                            background-color: #6d28d9;
                        }
                        QPushButton:pressed {
                            background-color: #5b21b6;
                        }
                    """)
                    edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    edit_btn.clicked.connect(lambda checked, fp=filepath: self.edit_invoice(fp))
                    actions_layout.addWidget(edit_btn)
                    
                    # Delete button
                    delete_btn = QPushButton("🗑️ Delete")
                    delete_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #dc2626;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            padding: 6px 12px;
                            font-weight: bold;
                            font-size: 12px;
                            min-width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #b91c1c;
                        }
                        QPushButton:pressed {
                            background-color: #991b1b;
                        }
                    """)
                    delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    delete_btn.clicked.connect(lambda checked, fp=filepath, r=row: self.delete_invoice(fp, r))
                    actions_layout.addWidget(delete_btn)
                    
                    # Download button
                    download_btn = QPushButton("💾")
                    download_btn.setToolTip("Download Invoice")
                    download_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.colors['accent_primary']};
                            color: white;
                            border: none;
                            border-radius: 5px;
                            padding: 6px 12px;
                            font-weight: bold;
                            font-size: 12px;
                            min-width: 40px;
                        }}
                        QPushButton:hover {{
                            background-color: {self.colors['accent_secondary']};
                        }}
                        QPushButton:pressed {{
                            background-color: {self.colors['accent_primary']};
                        }}
                    """)
                    download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    download_btn.clicked.connect(lambda checked, fp=filepath: self.download_invoice(fp))
                    actions_layout.addWidget(download_btn)
                    
                    self.invoice_table.setCellWidget(row, 5, actions_widget)
                    
                except Exception as e:
                    print(f"✗ Error loading invoice {filename}: {e}")
            
            print(f"✓ Loaded {self.invoice_table.rowCount()} invoices successfully")
                    
        except Exception as e:
            print(f"✗ Error loading invoices: {e}")
    
    def filter_invoices(self):
        """Filter invoices based on search text."""
        search_text = self.search_invoice.text().lower()
        
        for row in range(self.invoice_table.rowCount()):
            show_row = False
            
            for col in range(3):
                item = self.invoice_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            self.invoice_table.setRowHidden(row, not show_row)
    
    def download_invoice(self, filepath):
        """Download invoice to user-selected location."""
        try:
            import shutil
            
            filename = os.path.basename(filepath)
            
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Invoice",
                filename,
                "JSON Files (*.json);;All Files (*.*)"
            )
            
            if save_path:
                shutil.copy2(filepath, save_path)
                QMessageBox.information(self, "Success", f"Invoice downloaded successfully!\n{save_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download invoice:\n{str(e)}")
    
    def edit_invoice(self, filepath):
        """Edit an existing invoice."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Switch to Home page
            self.dashboard.content_stack.setCurrentIndex(0)
            
            # Load data into form
            self.dashboard.invoice_number.setText(data.get('invoice_number', ''))
            self.dashboard.customer_name.setText(data.get('customer_name', ''))
            self.dashboard.contact_number.setText(data.get('contact_number', ''))
            self.dashboard.customer_address.setText(data.get('customer_address', ''))
            
            # Parse date
            date_str = data.get('invoice_date', '')
            if date_str:
                try:
                    date_parts = date_str.split('/')
                    if len(date_parts) == 3:
                        day, month, year = map(int, date_parts)
                        self.dashboard.invoice_date.setDate(QDate(year, month, day))
                except:
                    pass
            
            # Clear existing rows
            self.dashboard.table.setRowCount(0)
            
            # Load items
            items = data.get('items', [])
            for item_data in items:
                self.dashboard.add_item_row()
                row = self.dashboard.table.rowCount() - 1
                
                # Set item values
                passenger_w = self.dashboard.table.cellWidget(row, 0)
                if passenger_w:
                    passenger_w.setText(item_data.get('passenger_name', ''))
                
                pnr_w = self.dashboard.table.cellWidget(row, 1)
                if pnr_w:
                    pnr_w.setText(item_data.get('pnr', ''))
                
                sector_w = self.dashboard.table.cellWidget(row, 2)
                if sector_w:
                    sector_w.setText(item_data.get('sector', ''))
                
                supplier_w = self.dashboard.table.cellWidget(row, 3)
                if supplier_w:
                    supplier_w.setCurrentText(item_data.get('supplier', ''))
                
                type_w = self.dashboard.table.cellWidget(row, 4)
                if type_w:
                    type_w.setText(item_data.get('type', ''))
                
                class_w = self.dashboard.table.cellWidget(row, 5)
                if class_w:
                    class_w.setCurrentText(item_data.get('class', ''))
                
                price_w = self.dashboard.table.cellWidget(row, 6)
                if price_w:
                    price_w.setValue(float(item_data.get('price', 0)))
                
                qty_w = self.dashboard.table.cellWidget(row, 7)
                if qty_w:
                    qty_w.setValue(float(item_data.get('qty', 1)))
                
                tax_w = self.dashboard.table.cellWidget(row, 8)
                if tax_w:
                    tax_w.setValue(float(item_data.get('tax', 0)))
            
            # Load payment details
            discount_text = data.get('discount', '₹0.00').replace('₹', '').replace(',', '').strip()
            self.dashboard.txt_discount.setText(discount_text)
            
            received_text = data.get('received', '₹0.00').replace('₹', '').replace(',', '').strip()
            self.dashboard.txt_received.setText(received_text)
            
            # Recalculate
            self.dashboard.update_invoice_totals()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load invoice for editing:\n{str(e)}")
    
    def delete_invoice(self, filepath, row):
        """Delete an invoice after confirmation."""
        try:
            invoice_num = os.path.basename(filepath).replace('invoice_', '').replace('.json', '')
            
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete invoice:\n\n{invoice_num}\n\n"
                "This action cannot be undone!",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                os.remove(filepath)
                self.invoice_table.removeRow(row)
                self.refresh_reports()
                
                QMessageBox.information(self, "Success", f"Invoice {invoice_num} deleted successfully!")
                
        except FileNotFoundError:
            QMessageBox.warning(self, "Not Found", "Invoice file not found. It may have already been deleted.")
            self.refresh_reports()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to delete invoice:\n{str(e)}")
