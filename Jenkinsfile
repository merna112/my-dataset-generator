pipeline {
    agent any

    stages {
        stage('Install System Dependencies') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-pip'
                sh 'ln -s /usr/bin/pip3 /usr/bin/pip || true'
            }
        }
        stage('Install Python Libraries') {
            steps {
                sh 'pip install pandas --break-system-packages'
            }
        }
        stage('Generate Dataset') {
            steps {
                sh 'python3 generate_advanced_repo_dataset.py'
            }
        }
        stage('Archive Dataset') {
            steps {
                archiveArtifacts artifacts: 'advanced_evaluation_data/*.csv', followSymlinks: false
            }
        }
    }
    post {
        always {
            echo "Pipeline finished with status: ${currentBuild.currentResult}"
        }
    }
}
