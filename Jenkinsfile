pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github_token')
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    pip3 install --user -r requirements.txt
                '''
            }
        }

        stage('Fetch Data from GitHub') {
            steps {
                sh '''
                    python3 fetch_github_data.py
                '''
            }
        }

        stage('Build Dataset') {
            steps {
                sh '''
                    python3 build_dataset.py
                '''
            }
        }

        stage('Validate Dataset') {
            steps {
                sh '''
                    python3 validate_dataset.py
                '''
            }
        }

        stage('Archive Dataset') {
            steps {
                archiveArtifacts artifacts: 'service_discovery_dataset.json', fingerprint: true
            }
        }
    }
}
