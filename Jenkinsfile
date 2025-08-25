pipeline {
    agent any

    stages {
        stage('Generate Semantic Dataset') {
            steps {
                // لم نعد بحاجة لتثبيت أي مكتبات خارجية
                // السكريبت الآن يعتمد فقط على مكتبات بايثون الأساسية
                sh 'python3 generate_semantic_dataset.py'
            }
        }
        stage('Archive Dataset') {
            steps {
                // تأكد من أن اسم المجلد هنا مطابق لما هو مكتوب في السكريبت
                archiveArtifacts artifacts: 'service_discovery_semantic_data/*.json', allowEmptyArchive: false
            }
        }
    }
    post {
        success {
            echo "Pipeline finished successfully. The semantic dataset is ready in the build artifacts."
        }
        failure {
            echo "Pipeline failed. Please check the console output for errors."
        }
    }
}
