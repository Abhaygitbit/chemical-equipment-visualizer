# 🧪 Chemical Equipment Parameter Visualizer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![React](https://img.shields.io/badge/React-18.2-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A professional full-stack application for analyzing chemical equipment performance data**

[Live Demo](#) • [Documentation](./QUICKSTART.md) • [API Docs](./API_DOCUMENTATION.md) • [Report Bug](#)

</div>

---

## 📖 About The Project

This hybrid application was developed as part of an internship screening task to demonstrate proficiency in full-stack development. It showcases the ability to build interconnected systems with a shared backend API serving multiple frontend platforms.

### 🎯 Problem Statement

Chemical engineers and facility managers need to:
- Quickly analyze equipment performance data from CSV files
- Visualize trends and distributions across equipment types
- Generate professional reports for stakeholders
- Access analysis tools both online and offline

### 💡 Solution

A unified backend API serving both a modern web application and a native desktop application, providing:
- **Instant Data Analysis** - Upload CSV and get immediate insights
- **Beautiful Visualizations** - Interactive charts for data exploration
- **Professional Reports** - One-click PDF generation
- **Flexible Access** - Use via browser or desktop application
- **Data Persistence** - Automatic history management

---

## ✨ Features

### Core Functionality
- ✅ **CSV Upload & Validation** - Smart file processing with error handling
- ✅ **Statistical Analysis** - Automatic calculation of averages and distributions
- ✅ **Data Visualization** - Multiple chart types (Pie, Bar, Tables)
- ✅ **PDF Reports** - Professional formatted reports with charts
- ✅ **Upload History** - Stores and manages last 5 datasets
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile

### Technical Features
- 🔌 **RESTful API** - Clean, documented endpoints
- 🎨 **Modern UI/UX** - Gradient themes and smooth animations
- 🚀 **Performance** - Multi-threaded operations for desktop app
- 🔒 **Data Validation** - Comprehensive input checking
- 📊 **Chart.js Integration** - Interactive web charts
- 📈 **Matplotlib Charts** - Professional desktop visualizations

---

## 🏗️ Architecture
```
┌─────────────────┐         ┌─────────────────┐
│  React Web App  │         │  PyQt5 Desktop  │
│   (Port 3000)   │         │      App        │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Django REST API     │
         │    (Port 8000)        │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   SQLite Database     │
         │   + Media Storage     │
         └───────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework 3.14** - API development
- **Pandas 2.1** - Data processing
- **ReportLab 4.0** - PDF generation
- **SQLite** - Database

### Web Frontend
- **React 18.2** - UI framework
- **Chart.js 4.4** - Data visualization
- **Axios** - HTTP client
- **CSS3** - Styling with gradients

### Desktop Frontend
- **PyQt5 5.15** - GUI framework
- **Matplotlib 3.8** - Charting library
- **Requests** - API communication

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/chemical-equipment-visualizer.git
   cd chemical-equipment-visualizer
```

2. **Backend Setup**
```bash
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
```

3. **Web Frontend Setup**
```bash
   cd frontend-web
   npm install
   npm start
```

4. **Desktop Application Setup**
```bash
   cd frontend-desktop
   pip install -r requirements.txt
   python main.py
```

### Sample Data

Use the included `sample_equipment_data.csv` to test the application.

---

## 📊 Usage Examples

### CSV File Format
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,180.2
Pump-C3,Pump,180.3,35.0,85.0
Heat Exchanger-B2,Heat Exchanger,220.0,18.5,120.5
```

### API Endpoints
```bash
# Health Check
GET /api/health/

# Upload CSV
POST /api/upload/

# Get Dataset
GET /api/datasets/{id}/

# Download PDF
GET /api/datasets/{id}/pdf/
```

See [API Documentation](./API_DOCUMENTATION.md) for complete reference.

---

## 🎨 Screenshots

### Web Application
![Web Dashboard](screenshots/web-dashboard.png)

### Desktop Application  
![Desktop App](screenshots/desktop-app.png)

---

## 📝 Project Structure
```
chemical-equipment-visualizer/
├── backend/                 # Django REST API
├── frontend-web/            # React application
├── frontend-desktop/        # PyQt5 application
├── sample_equipment_data.csv
├── README.md
└── Documentation/
    ├── QUICKSTART.md
    ├── API_DOCUMENTATION.md
    └── DEPLOYMENT.md
```

---

## 🧪 Testing
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend-web
npm test
```

---

## 🚢 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment guides:
- Heroku / Railway (Backend)
- Vercel / Netlify (Frontend)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourname)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Sample data inspired by industrial chemical processing
- UI design influenced by modern material design
- Built as part of internship screening task

---

## 📞 Support

If you found this project helpful, please give it a ⭐!

For questions or issues, please [open an issue](https://github.com/yourusername/chemical-equipment-visualizer/issues).

---

<div align="center">
Made with ❤️ for Chemical Engineers
</div>
```

---

## 🏷️ GitHub Topics/Tags

Add these tags to your repository:
```
django, react, pyqt5, data-visualization, chemical-engineering, 
rest-api, full-stack, python, javascript, hybrid-application, 
csv-processing, pandas, chartjs, matplotlib, pdf-generation, 
internship-project, portfolio
