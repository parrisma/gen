from kafka import KafkaAdminClient

admin = KafkaAdminClient(bootstrap_servers=['localhost:32561'],
                         api_version=(0, 2, 13))

print(admin)
