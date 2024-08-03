# import.sh
#!/bin/bash

function check_mongo() {
  mongo --eval 'db.adminCommand("isMaster").primary' &> /dev/null
  if [ $? -eq 0 ]; then
    echo "MongoDB is running"
    return 0
  fi
  echo "MongoDB not running yet"
  sleep 2
}

while ! check_mongo; do
  echo "Waiting for MongoDB..."
done

mongoimport --db test --collection university_schema --type csv --file UniversitySchema.csv --headerline
