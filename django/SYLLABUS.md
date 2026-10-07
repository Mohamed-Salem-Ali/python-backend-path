# Django syllabus

Weeks 5–9 of the [12-week plan](../docs/12-week-plan.md). Prerequisite: the [Python exit exam](../python/SYLLABUS.md#exit-exam-i-know-python).

**Level target:** build, test, secure and deploy a Django application with a REST API, and explain how a request moves through the framework.

**Project:** Gameya, a rotating-savings (gameya) tracker, built up module by module. Each module adds one capability and its tests.

## Core track

| Week | Module | You can… |
|---|---|---|
| 5 | Architecture | explain MTV, project vs app, settings, URL routing, the request/response cycle |
| 5 | Models and ORM | define models and relations, write migrations, use QuerySets, managers and aggregation |
| 6 | Admin and forms | configure the admin, write forms and validation |
| 6 | Views and templates | choose between function and class-based views; render templates with inheritance |
| 7 | Middleware and signals | write middleware; use signals (and know when not to) |
| 7 | Testing | test with pytest-django, factories and the test client |
| 7 | Caching and performance | find and fix N+1 queries (`select_related`, `prefetch_related`), use the cache framework |
| 8 | Django REST Framework | serializers, viewsets and routers, permissions, auth, pagination, filtering |
| 9 | Background tasks | run Celery tasks, schedule jobs |
| 9 | Auth and security | sessions vs JWT, CSRF, XSS, ownership permissions, secure settings |
| 9 | Deployment | gunicorn, static files, env-driven settings, deploy to a real host |

## Exit exam: "I know Django"
- [ ] Trace a request from the URL to the response, naming each layer it passes through
- [ ] Add a model field, generate and apply a migration, and explain what the migration file contains
- [ ] Take a view that issues 101 queries and bring it to 2, showing the query count before and after
- [ ] Write a permission that only lets the owner edit an object, with tests
- [ ] Write a DRF endpoint with a serializer, validation, pagination and filtering
- [ ] Explain CSRF, and why a JSON API using JWT does not need it the same way
- [ ] Deploy the project with environment-based settings and a production database

## Advanced tier (after week 12)
- Query tuning: `EXPLAIN`, indexes, `only/defer`, bulk operations, database constraints
- Concurrency in the database: `select_for_update`, transactions, race conditions
- Scaling: caching layers, read replicas, async views, Celery at scale and retries
- Architecture: service layers, custom managers, multi-tenancy, feature flags
- Operations: logging, Sentry, health checks, zero-downtime migrations
- Contribute: read Django's own source for the ORM and the request path
