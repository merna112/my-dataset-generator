pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-pip'
                sh 'pip install pandas --break-system-packages' 
            }
        }
        stage('Generate Service Discovery Dataset') {
            steps {
                sh 'python3 generate_service_discovery_dataset.py'
            }
        }
        stage('Archive Dataset') {
            steps {
                archiveArtifacts artifacts: 'service_discovery_data/*.json', followSymlinks: false
            }
        }
    }
}
