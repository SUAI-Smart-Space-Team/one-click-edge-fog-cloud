pipeline 
{
    agent 
    {
       label 'ocefc'
    }
    stages 
    {
        stage("building")
        {
            steps
            {
                sh 'python3.9 main.py $configurator $module $action'
            }
        }
    }
}
