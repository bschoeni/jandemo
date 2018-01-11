
import web
import json

from neo4j.v1 import GraphDatabase

urls = (
    '/', 'index',
    '/employees', 'employees'
)

uri = "bolt://localhost:7687"

driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

class index:
    def GET(self):
        return "Welome to a demo neo4j REST API!"

class employees:
    def GET(self):
	with driver.session() as session:
                jstr = "{\n\t\"employees\": [\n"
		for record in session.run("MATCH (e: Employee) RETURN e.name, e.emp_id;"):
			str = json.dumps({ "name" : record["e.name"], "emp_id" : int(record["e.emp_id"])})
                        if len(jstr) > 18:
				jstr += "\t\t,"
			else:
				jstr += "\t\t"
                        jstr += str + '\n'
                jstr += "\n\t]\n}"
                return jstr

    def POST(self):
        data = web.input()
        name, id = data.name, data.id
	with driver.session() as session:
        	with session.begin_transaction() as tx:
        		result = tx.run('CREATE (a:Employee { name: \"%s\", emp_id: %d} ) RETURN id(a);' % (name, int(id)))
        return "POST %s %s" % (name, id)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
