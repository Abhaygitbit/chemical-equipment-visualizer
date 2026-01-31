import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

API_URL = "http://localhost:8000/api"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 1200, 800)
    
        # Create tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Upload tab
        self.upload_tab = QWidget()
        self.create_upload_tab()
        self.tabs.addTab(self.upload_tab, "📤 Upload")
        
        # Dashboard tab
        self.dashboard_tab = QWidget()
        self.create_dashboard_tab()
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        
        self.dataset = None
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
            QTabWidget::pane {
                border: none;
                background: white;
                border-radius: 10px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 15px 30px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QTabBar::tab:selected {
                background: white;
            }
        """)
    
    def create_upload_tab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Upload Equipment Data')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Upload button
        self.upload_btn = QPushButton('📂 Select CSV File')
        self.upload_btn.clicked.connect(self.select_file)
        layout.addWidget(self.upload_btn)
        
        # File label
        self.file_label = QLabel('No file selected')
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)
        
        # Upload button
        self.submit_btn = QPushButton('🚀 Upload and Analyze')
        self.submit_btn.clicked.connect(self.upload_file)
        self.submit_btn.setEnabled(False)
        layout.addWidget(self.submit_btn)
        
        layout.addStretch()
        self.upload_tab.setLayout(layout)
        
        self.selected_file = None
    
    def create_dashboard_tab(self):
        layout = QVBoxLayout()
        
        # Title
        self.dash_title = QLabel('No data loaded')
        self.dash_title.setFont(QFont('Arial', 20, QFont.Bold))
        self.dash_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.dash_title)
        
        # Summary cards
        cards_layout = QHBoxLayout()
        self.total_label = self.create_card('Total', '0')
        self.flow_label = self.create_card('Avg Flowrate', '0')
        self.pressure_label = self.create_card('Avg Pressure', '0')
        self.temp_label = self.create_card('Avg Temp', '0')
        
        cards_layout.addWidget(self.total_label)
        cards_layout.addWidget(self.flow_label)
        cards_layout.addWidget(self.pressure_label)
        cards_layout.addWidget(self.temp_label)
        layout.addLayout(cards_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Pie chart
        self.pie_canvas = FigureCanvas(plt.Figure(figsize=(5, 4)))
        charts_layout.addWidget(self.pie_canvas)
        
        # Bar chart
        self.bar_canvas = FigureCanvas(plt.Figure(figsize=(5, 4)))
        charts_layout.addWidget(self.bar_canvas)
        
        layout.addLayout(charts_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        layout.addWidget(self.table)
        
        # PDF button
        self.pdf_btn = QPushButton('📄 Download PDF')
        self.pdf_btn.clicked.connect(self.download_pdf)
        layout.addWidget(self.pdf_btn)
        
        self.dashboard_tab.setLayout(layout)
    
    def create_card(self, title, value):
        card = QGroupBox()
        card.setStyleSheet("""
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 12))
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV', '', 'CSV Files (*.csv)')
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f'Selected: {file_path.split("/")[-1]}')
            self.submit_btn.setEnabled(True)
    
    def upload_file(self):
        if not self.selected_file:
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{API_URL}/upload/', files=files)
                
            if response.status_code == 201:
                self.dataset = response.json()['data']
                self.update_dashboard()
                self.tabs.setCurrentIndex(1)
                QMessageBox.information(self, 'Success', 'File uploaded successfully!')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Upload failed'))
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def update_dashboard(self):
        if not self.dataset:
            return
        
        # Update title
        self.dash_title.setText(f'Dashboard - {self.dataset["filename"]}')
        
        # Update cards
        self.update_card_value(self.total_label, str(self.dataset['total_count']))
        self.update_card_value(self.flow_label, f"{self.dataset['averages']['flowrate']:.2f}")
        self.update_card_value(self.pressure_label, f"{self.dataset['averages']['pressure']:.2f}")
        self.update_card_value(self.temp_label, f"{self.dataset['averages']['temperature']:.2f}")
        
        # Update pie chart
        self.pie_canvas.figure.clear()
        ax1 = self.pie_canvas.figure.add_subplot(111)
        types = list(self.dataset['type_distribution'].keys())
        counts = list(self.dataset['type_distribution'].values())
        ax1.pie(counts, labels=types, autopct='%1.1f%%')
        ax1.set_title('Equipment Type Distribution')
        self.pie_canvas.draw()
        
        # Update bar chart
        self.bar_canvas.figure.clear()
        ax2 = self.bar_canvas.figure.add_subplot(111)
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.dataset['averages']['flowrate'],
            self.dataset['averages']['pressure'],
            self.dataset['averages']['temperature']
        ]
        ax2.bar(params, values, color=['#667eea', '#764ba2', '#ff6b6b'])
        ax2.set_title('Average Parameters')
        self.bar_canvas.draw()
        
        # Update table
        equipment = self.dataset.get('equipment_list', [])
        self.table.setRowCount(len(equipment))
        for i, eq in enumerate(equipment):
            self.table.setItem(i, 0, QTableWidgetItem(eq['name']))
            self.table.setItem(i, 1, QTableWidgetItem(eq['type']))
            self.table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.2f}"))
    
    def update_card_value(self, card, value):
        layout = card.layout()
        value_label = layout.itemAt(1).widget()
        value_label.setText(value)
    
    def download_pdf(self):
        if not self.dataset:
            return
        
        try:
            response = requests.get(f"{API_URL}/datasets/{self.dataset['id']}/pdf/")
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save PDF', f"report_{self.dataset['id']}.pdf", 'PDF Files (*.pdf)')
            
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                QMessageBox.information(self, 'Success', 'PDF downloaded!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())