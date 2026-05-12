pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\bbudy\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
    }

    stages {
        stage('Install dependencies') {
            steps {
                powershell '''
                & "$env:PYTHON_EXE" -m venv .venv
                .\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
                .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt pytest
                '''
            }
        }

        stage('Run tests') {
            steps {
                powershell '''
                .\\.venv\\Scripts\\python.exe -m pytest -v
                '''
            }
        }
    }
}