// this pipeline contains a few plugin dependencies you need to resolve on Jenkins:
// - sshCommand
// - ansiColor
// you also need to point Jenkins to Terraform (validated with 0.11.latest)
// you need to create a username/password credentials set that sshCommand will use
// that's about it - enjoy!

void slackTalk(msg) {
    // if you want to use Slack, add an integration (webhook-type) to your channel
    // you will receive values for T, B and S
    T = "TQD55T6UF"
    B = "BQ0K1GBGB"
    S= "oVbsstox4mp30MKNgI28d6NR"
    sh "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"${msg}\"}' https://hooks.slack.com/services/$T/$B/$S"
}


pipeline {
 agent any
 tools {
    "org.jenkinsci.plugins.terraform.TerraformInstallation" "terraform"
 }

 environment {
    TF_HOME = tool('terraform')
    TF_IN_AUTOMATION = "true"
    PATH = "$TF_HOME:$PATH"
    // TF_LOG controls the level of debugging in Terraform
    TF_LOG = "INFO"
 }
 
 stages {
   stage('Git code checkout'){
     steps {
       dir('dev'){
         ansiColor('xterm'){
           git branch: 'master', url: 'http://10.67.185.80/cisco/camrossi/cicd.git'
         }
       }
     }
   }
 
   stage('Terraform Init for the ACI plan'){
     steps {
       dir('dev/ACI'){
         ansiColor('xterm'){
           sh "terraform init -input=false -force-copy -upgrade"
           sh "echo \$PWD" 
         }    
       }
     }
   }

   stage('Terraform Init for the VMWARE plan'){
     steps {
       dir('dev/VMWARE'){
         ansiColor('xterm'){
           sh "terraform init -input=false -force-copy -upgrade"
           sh "echo \$PWD" 
         }    
       }
     }
   }


   stage('Terraform Plan for ACI') {
     steps {
       dir('dev/ACI'){ 
         ansiColor('xterm') {
           sh 'terraform plan -out=plan'
         }
       }
     }
   }

   stage('Apply ACI plan') {
     steps {
       dir('dev/ACI'){
         ansiColor('xterm'){
#           sh 'terraform apply -auto-approve'
            sh 'python aci.py'
         }
       }
     }
   }
   
//   stage('Terraform Destroy plan for VMware') {
//     steps {
//       dir('dev/VMWARE'){
//         ansiColor('xterm'){
//           sh 'terraform plan -destroy -out=plan'
//         }
//       }
//     }
//   }
//    
//   stage('Destroy VMware plan') {
//     steps {
//       script{
//         dir('dev/VMWARE'){
//           ansiColor('xterm'){
//             sh 'terraform apply -auto-approve'
//           }
//         }
//       }
//     }
//   }

   stage('Terraform plan for VMware') {
     steps {
       dir('dev/VMWARE'){
         ansiColor('xterm'){
           sh 'terraform plan -out=plan'
         }
       }
     }
   }


   stage('Apply VMware plan') {
     steps {
       script{
         dir('dev/VMWARE'){
           ansiColor('xterm'){
             sh 'terraform apply -auto-approve'
           }
         }
       }
     }
   }


   
   stage('Launch web server'){
     steps{
       script{
     def client = [:]
     client.name = "1.1.1.100"
     client.host = "1.1.1.100"
     client.allowAnyHosts = true
     def server = [:]
     server.name = "1.1.1.200"
     server.host = "1.1.1.200"
     server.allowAnyHosts = true
     withCredentials([usernamePassword(credentialsId: 'sshUserAccount', passwordVariable: 'password', usernameVariable: 'userName')]) {
         server.user = userName
         server.password = password
         client.user = userName
         client.password = password
         stage("SSH into Web Server") {
           script{
             try {
               timeout(time: 30, unit: 'SECONDS') {
                 sshCommand remote: server, command: '/home/cisco/start_app.sh &' 
               }
             } catch (err){
                 // we actually will enter the timeout phase
                 // that is because SSH command starts a shell which keeps hanging there forever
                 // after 30 seconds, we exit and end up here where we test app.py
                 def res = sshCommand remote: server, command: 'curl -s http://1.1.1.200:8080/hello'
                 if (res.equals("<h1>You have reached the hello page</h1>")){
                   // currentBuild.result = 'SUCCESS'
                 } else{
                     currentBuild.result = 'FAILURE'
                   }
                   
               }
           }   
         }            
       }
       stage("Validate ACI contract") {
           script{
               def res = sshCommand remote: client, command: 'curl -s http://1.1.1.200:8080/hello' 
               if (res.equals("<h1>You have reached the hello page</h1>")){
                   // currentBuild.result = 'SUCCESS'
                 } else{
                     currentBuild.result = 'FAILURE'
                   }
           }
       }
         
     } 
    }
   }

  } 
} 
