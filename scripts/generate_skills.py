import json
import os

skills_data = [
    ('Python', 'Programming', ['python', 'python3'], 'Programming Language'),
    ('R', 'Programming', ['r', 'r programming', 'r language'], 'Programming Language'),
    ('Java', 'Programming', ['java'], 'Programming Language'),
    ('C++', 'Programming', ['c++', 'cpp'], 'Programming Language'),
    ('C#', 'Programming', ['c#', 'c-sharp', 'csharp'], 'Programming Language'),
    ('JavaScript', 'Programming', ['javascript', 'js'], 'Programming Language'),
    ('TypeScript', 'Programming', ['typescript', 'ts'], 'Programming Language'),
    ('Go', 'Programming', ['go', 'golang'], 'Programming Language'),
    ('C', 'Programming', ['c', 'c language'], 'Programming Language'),
    ('Scala', 'Programming', ['scala'], 'Programming Language'),
    ('Ruby', 'Programming', ['ruby'], 'Programming Language'),
    ('PHP', 'Programming', ['php'], 'Programming Language'),
    ('Swift', 'Programming', ['swift'], 'Programming Language'),
    ('Kotlin', 'Programming', ['kotlin'], 'Programming Language'),
    ('Rust', 'Programming', ['rust'], 'Programming Language'),
    
    ('Machine Learning', 'Data Science', ['machine learning', 'ml'], 'Data Science'),
    ('Deep Learning', 'Data Science', ['deep learning', 'dl'], 'Data Science'),
    ('Natural Language Processing', 'Data Science', ['natural language processing', 'nlp'], 'Data Science'),
    ('Computer Vision', 'Data Science', ['computer vision', 'cv'], 'Data Science'),
    ('Statistics', 'Data Science', ['statistics', 'statistical modeling'], 'Mathematics'),
    ('Data Analysis', 'Data Science', ['data analysis', 'data analytics'], 'Data Science'),
    ('Data Visualization', 'Data Science', ['data visualization', 'data viz'], 'Data Science'),
    ('Predictive Modeling', 'Data Science', ['predictive modeling', 'predictive analytics'], 'Data Science'),
    ('Regression', 'Data Science', ['regression', 'linear regression', 'logistic regression'], 'Machine Learning'),
    ('Classification', 'Data Science', ['classification'], 'Machine Learning'),
    ('Clustering', 'Data Science', ['clustering', 'k-means'], 'Machine Learning'),
    ('Time Series', 'Data Science', ['time series', 'time series analysis', 'forecasting'], 'Data Science'),
    ('A/B Testing', 'Data Science', ['a/b testing', 'ab testing', 'hypothesis testing'], 'Data Science'),
    
    ('SQL', 'Data Engineering', ['sql', 'structured query language'], 'Database'),
    ('ETL', 'Data Engineering', ['etl', 'extract transform load', 'data pipelines', 'data pipeline'], 'Data Engineering'),
    ('Data Warehousing', 'Data Engineering', ['data warehousing', 'data warehouse'], 'Data Engineering'),
    ('Data Modeling', 'Data Engineering', ['data modeling'], 'Data Engineering'),
    
    ('Pandas', 'Frameworks', ['pandas'], 'Python Data Science'),
    ('NumPy', 'Frameworks', ['numpy'], 'Python Data Science'),
    ('SciPy', 'Frameworks', ['scipy'], 'Python Data Science'),
    ('Matplotlib', 'Frameworks', ['matplotlib'], 'Python Data Science'),
    ('Seaborn', 'Frameworks', ['seaborn'], 'Python Data Science'),
    ('Plotly', 'Frameworks', ['plotly'], 'Python Data Science'),
    
    ('Scikit-learn', 'Frameworks', ['scikit-learn', 'sklearn', 'scikit learn'], 'Machine Learning Framework'),
    ('PyTorch', 'Frameworks', ['pytorch', 'torch'], 'Machine Learning Framework'),
    ('TensorFlow', 'Frameworks', ['tensorflow', 'tf'], 'Machine Learning Framework'),
    ('Keras', 'Frameworks', ['keras'], 'Machine Learning Framework'),
    ('XGBoost', 'Frameworks', ['xgboost', 'xgb'], 'Machine Learning Framework'),
    ('LightGBM', 'Frameworks', ['lightgbm', 'lgbm'], 'Machine Learning Framework'),
    ('CatBoost', 'Frameworks', ['catboost'], 'Machine Learning Framework'),
    ('Hugging Face', 'Frameworks', ['hugging face', 'huggingface', 'transformers'], 'Machine Learning Framework'),
    ('OpenCV', 'Frameworks', ['opencv', 'cv2'], 'Machine Learning Framework'),
    
    ('PostgreSQL', 'Database', ['postgresql', 'postgres', 'postgres db'], 'SQL Database'),
    ('MySQL', 'Database', ['mysql'], 'SQL Database'),
    ('MongoDB', 'Database', ['mongodb', 'mongo'], 'NoSQL Database'),
    ('SQLite', 'Database', ['sqlite'], 'SQL Database'),
    ('Redis', 'Database', ['redis'], 'NoSQL Database'),
    ('SQL Server', 'Database', ['sql server', 'mssql', 'microsoft sql server'], 'SQL Database'),
    ('Oracle', 'Database', ['oracle db', 'oracle database', 'oracle'], 'SQL Database'),
    ('Cassandra', 'Database', ['cassandra', 'apache cassandra'], 'NoSQL Database'),
    ('DynamoDB', 'Database', ['dynamodb'], 'NoSQL Database'),
    ('Snowflake', 'Database', ['snowflake'], 'Data Warehouse'),
    ('Redshift', 'Database', ['redshift', 'amazon redshift'], 'Data Warehouse'),
    ('BigQuery', 'Database', ['bigquery', 'google bigquery'], 'Data Warehouse'),
    
    ('AWS', 'Cloud', ['aws', 'amazon web services'], 'Cloud Platform'),
    ('Azure', 'Cloud', ['azure', 'microsoft azure'], 'Cloud Platform'),
    ('GCP', 'Cloud', ['gcp', 'google cloud platform', 'google cloud'], 'Cloud Platform'),
    ('EC2', 'Cloud', ['ec2', 'amazon ec2'], 'Cloud Services'),
    ('S3', 'Cloud', ['s3', 'amazon s3'], 'Cloud Services'),
    ('Lambda', 'Cloud', ['lambda', 'aws lambda'], 'Cloud Services'),
    
    ('Power BI', 'BI', ['power bi', 'powerbi'], 'Business Intelligence'),
    ('Tableau', 'BI', ['tableau'], 'Business Intelligence'),
    ('Looker', 'BI', ['looker'], 'Business Intelligence'),
    ('Qlik', 'BI', ['qlik', 'qlikview', 'qliksense'], 'Business Intelligence'),
    
    ('Docker', 'DevOps', ['docker', 'containerization'], 'DevOps'),
    ('Kubernetes', 'DevOps', ['kubernetes', 'k8s'], 'DevOps'),
    ('Git', 'DevOps', ['git', 'version control'], 'DevOps'),
    ('GitHub', 'DevOps', ['github'], 'DevOps'),
    ('GitLab', 'DevOps', ['gitlab'], 'DevOps'),
    ('Bitbucket', 'DevOps', ['bitbucket'], 'DevOps'),
    ('CI/CD', 'DevOps', ['ci/cd', 'ci-cd', 'continuous integration', 'continuous deployment'], 'DevOps'),
    ('Jenkins', 'DevOps', ['jenkins'], 'DevOps'),
    ('Terraform', 'DevOps', ['terraform'], 'DevOps'),
    ('Ansible', 'DevOps', ['ansible'], 'DevOps'),
    
    ('React', 'Frameworks', ['react', 'react.js', 'reactjs'], 'Web Framework'),
    ('Next.js', 'Frameworks', ['next.js', 'nextjs'], 'Web Framework'),
    ('Node.js', 'Frameworks', ['node.js', 'nodejs', 'node'], 'Web Framework'),
    ('Django', 'Frameworks', ['django'], 'Web Framework'),
    ('Flask', 'Frameworks', ['flask'], 'Web Framework'),
    ('FastAPI', 'Frameworks', ['fastapi'], 'Web Framework'),
    ('Spring Boot', 'Frameworks', ['spring boot', 'springboot', 'spring'], 'Web Framework'),
    ('.NET', 'Frameworks', ['.net', 'dotnet', '.net core'], 'Web Framework'),
    ('Vue.js', 'Frameworks', ['vue', 'vue.js', 'vuejs'], 'Web Framework'),
    ('Angular', 'Frameworks', ['angular', 'angular.js'], 'Web Framework'),
    
    ('Spark', 'Big Data', ['spark', 'apache spark', 'pyspark'], 'Big Data'),
    ('Hadoop', 'Big Data', ['hadoop', 'apache hadoop'], 'Big Data'),
    ('Kafka', 'Big Data', ['kafka', 'apache kafka'], 'Big Data'),
    ('Airflow', 'Big Data', ['airflow', 'apache airflow'], 'Data Engineering'),
    ('Databricks', 'Big Data', ['databricks'], 'Big Data'),
    ('Flume', 'Big Data', ['flume', 'apache flume'], 'Big Data'),
    ('Hive', 'Big Data', ['hive', 'apache hive'], 'Big Data'),
    ('Pig', 'Big Data', ['pig', 'apache pig'], 'Big Data'),
    ('Flink', 'Big Data', ['flink', 'apache flink'], 'Big Data'),
    ('NiFi', 'Big Data', ['nifi', 'apache nifi'], 'Big Data'),
    
    # Testing & QA
    ('Selenium', 'Testing', ['selenium', 'selenium webdriver'], 'Software Testing'),
    ('Cypress', 'Testing', ['cypress'], 'Software Testing'),
    ('Jest', 'Testing', ['jest'], 'Software Testing'),
    ('Mocha', 'Testing', ['mocha'], 'Software Testing'),
    ('PyTest', 'Testing', ['pytest', 'py.test'], 'Software Testing'),
    ('JUnit', 'Testing', ['junit'], 'Software Testing'),
    ('TestNG', 'Testing', ['testng'], 'Software Testing'),
    ('Appium', 'Testing', ['appium'], 'Software Testing'),
    ('Cucumber', 'Testing', ['cucumber'], 'Software Testing'),
    
    # OS & Environments
    ('Linux', 'OS', ['linux', 'ubuntu', 'debian', 'centos', 'redhat', 'rhel'], 'Operating System'),
    ('Windows', 'OS', ['windows', 'windows server'], 'Operating System'),
    ('macOS', 'OS', ['macos', 'mac os x', 'osx'], 'Operating System'),
    ('Unix', 'OS', ['unix'], 'Operating System'),
    ('Bash', 'OS', ['bash', 'bash scripting', 'shell scripting', 'shell script'], 'Scripting'),
    ('PowerShell', 'OS', ['powershell'], 'Scripting'),
    
    # Cloud & Infrastructure (More)
    ('DigitalOcean', 'Cloud', ['digitalocean', 'digital ocean'], 'Cloud Platform'),
    ('Heroku', 'Cloud', ['heroku'], 'Cloud Platform'),
    ('Vagrant', 'DevOps', ['vagrant'], 'DevOps'),
    ('Puppet', 'DevOps', ['puppet'], 'DevOps'),
    ('Chef', 'DevOps', ['chef'], 'DevOps'),
    ('Prometheus', 'DevOps', ['prometheus'], 'Monitoring'),
    ('Grafana', 'DevOps', ['grafana'], 'Monitoring'),
    ('Datadog', 'DevOps', ['datadog'], 'Monitoring'),
    ('Splunk', 'DevOps', ['splunk'], 'Monitoring'),
    ('ELK Stack', 'DevOps', ['elk', 'elk stack', 'elasticsearch', 'logstash', 'kibana'], 'Monitoring'),
    
    # Soft Skills & Project Management
    ('Agile', 'Methodology', ['agile', 'agile methodology', 'scrum'], 'Project Management'),
    ('Kanban', 'Methodology', ['kanban'], 'Project Management'),
    ('Jira', 'Methodology', ['jira', 'atlassian jira'], 'Project Management'),
    ('Confluence', 'Methodology', ['confluence'], 'Project Management'),
    ('Trello', 'Methodology', ['trello'], 'Project Management'),
    ('Problem Solving', 'Soft Skills', ['problem solving', 'problem-solving'], 'Soft Skills'),
    ('Communication', 'Soft Skills', ['communication', 'communication skills'], 'Soft Skills'),
    ('Teamwork', 'Soft Skills', ['teamwork', 'team collaboration'], 'Soft Skills'),
    ('Leadership', 'Soft Skills', ['leadership', 'team leading'], 'Soft Skills'),
    
    # Security
    ('Cybersecurity', 'Security', ['cybersecurity', 'cyber security', 'infosec'], 'Information Security'),
    ('Penetration Testing', 'Security', ['penetration testing', 'pen testing'], 'Information Security'),
    ('Cryptography', 'Security', ['cryptography'], 'Information Security'),
    ('OAuth', 'Security', ['oauth', 'oauth2'], 'Authentication'),
    ('JWT', 'Security', ['jwt', 'json web token'], 'Authentication'),
    
    # Web Technologies (Basics)
    ('HTML', 'Web', ['html', 'html5'], 'Web Development'),
    ('CSS', 'Web', ['css', 'css3'], 'Web Development'),
    ('SASS', 'Web', ['sass', 'scss'], 'Web Development'),
    ('LESS', 'Web', ['less'], 'Web Development'),
    ('Tailwind CSS', 'Web', ['tailwind', 'tailwindcss'], 'Web Development'),
    ('Bootstrap', 'Web', ['bootstrap'], 'Web Development'),
    ('REST', 'Web', ['rest', 'restful', 'rest api', 'restful api'], 'Web Services'),
    ('GraphQL', 'Web', ['graphql'], 'Web Services'),
    ('SOAP', 'Web', ['soap'], 'Web Services'),
    ('WebSockets', 'Web', ['websockets', 'websocket'], 'Web Services'),
    
    # Mobile
    ('Android', 'Mobile', ['android', 'android development'], 'Mobile Development'),
    ('iOS', 'Mobile', ['ios', 'ios development'], 'Mobile Development'),
    ('React Native', 'Mobile', ['react native'], 'Mobile Development'),
    ('Flutter', 'Mobile', ['flutter'], 'Mobile Development'),
    ('Dart', 'Programming', ['dart'], 'Programming Language')
]

out = {}
for canonical, category, aliases, generic_parent in skills_data:
    key = canonical.lower()
    out[key] = {
        'canonical': canonical,
        'category': category,
        'aliases': aliases,
        'generic_parent': generic_parent
    }
    
os.makedirs('data', exist_ok=True)
with open('data/skills.json', 'w') as f:
    json.dump(out, f, indent=2)
print('Generated data/skills.json with', len(out), 'skills')
