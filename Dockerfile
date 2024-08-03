# Use the official MongoDB image (latest tag)
FROM mongo

# Copy the UniversitySchema.csv file into the container's directory where MongoDB stores data
COPY UniversitySchema.csv /docker-entrypoint-initdb.d/

# The mongoimport command will be executed when the container starts
CMD mongoimport --host localhost --db university_data --collection courses --type csv --headerline --file /docker-entrypoint-initdb.d/UniversitySchema.csv
