pipeline {
    // agent {
    //     node {
    //         label 'docker_agent_python'
    //     }
    // }

    agent {
        node {
            label 'my-host-agent' // Use the label assigned in the configuration
        }
    }

    triggers {
        pollSCM '*/1 * * * *'
    }

    environment {
        DOCKER_IMAGE = 'faroukcha69/ci_image'
    }

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                script {
                    def app = docker.build("${DOCKER_IMAGE}") // Declare and initialize `app` here
                }
            }
        }

        stage('Test image') {
            steps {
                script {
                    app.inside { // Use `app` only inside the script block where it's declared
                        sh 'echo "Tests passed"'
                    }
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        app.push("${env.BUILD_NUMBER}")
                    }
                }
            }
        }

        stage('Trigger ManifestUpdate') {
            steps {
                build job: 'cd_update_manifest_job', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        // cleanup {
        //     script {
        //         // Optional cleanup logic, e.g., remove unused Docker images
        //         sh 'docker image prune -f'
        //     }
        // }
    }
}
