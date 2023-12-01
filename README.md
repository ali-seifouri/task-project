# task-project
We want to build a project from scratch like Jira. There, we will have the entity 'task.' The requirements for this entity are as follows:
In a task, there can be static fields (that users cannot remove or add, e.g., id, name, description, status) and 'custom fields' that users can add as many as they want.
Custom fields can have different types: text, int, date, links to users, etc.
Users will perform CRUD operations, especially listing tasks and filtering them by combinations of static/custom fields.
We may have 1 million or more tasks in one company.

-----------------------------------------------------

With afrementioned requirements a proper solution for database would be MongoDB because the data schema is dynamic.
also it can be easily horizontally scaled and sharded.
One problem was auto generated ObjectId field, because it is hard to serialize.
I used aggregation pipelines in mongodb, so the data was converted to string, it's a clean solution.
