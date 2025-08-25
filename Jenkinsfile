pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-pip'
                sh 'pip install pandas --break-system-packages'
            }
        }
        stage('Generate and Debug Dataset') {
            steps {
                // شغّل السكريبت واكتب كل مخرجاته وأخطائه في ملف اسمه script.log
                sh 'python3 generate_service_discovery_dataset.py > script.log 2>&1'
            }
        }
        stage('Display Log and Archive') {
            steps {
                // اعرض محتويات ملف السجل لنرى الخطأ الحقيقي
                sh 'cat script.log'
                archiveArtifacts artifacts: 'service_discovery_data/*.json', allowEmptyArchive: true
            }
        }
    }
}
