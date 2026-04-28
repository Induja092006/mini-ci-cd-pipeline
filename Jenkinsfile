pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t flask-docker-app .'
            }
        }

        stage('Stop & Clean Old Container') {
            steps {
                script {
                    bat 'docker stop test-app || exit /b 0'
                    bat 'docker rm -f test-app || exit /b 0'
                    bat 'docker container prune -f'
                }
                // Proper delay (instead of ping/timeout issue)
                sleep(time: 3, unit: 'SECONDS')
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // short delay before run
                    sleep(time: 2, unit: 'SECONDS')

                    bat 'docker run -d -p 5000:5000 --name test-app flask-docker-app'
                    echo "App running at: http://localhost:5000"
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    // wait for app startup
                    sleep(time: 5, unit: 'SECONDS')

                    bat 'curl http://localhost:5000 || exit /b 1'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo '✅ Deployment Successful!'
        }
        failure {
            echo '❌ Deployment Failed!'
        }
    }
}
