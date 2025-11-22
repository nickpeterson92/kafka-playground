# Task Completion Checklist

## Code Quality Steps

When completing a development task, follow these steps:

### 1. Format Code
```bash
black .
```
- Run Black formatter on entire codebase
- Ensures consistent code style

### 2. Lint Code
```bash
ruff check .
```
- Check for code quality issues
- Fix any reported problems before committing

### 3. Type Check
```bash
mypy .
```
- Verify type annotations are correct
- Resolve any type errors

### 4. Run Tests (When Available)
```bash
pytest
```
- Ensure all tests pass
- Add tests for new functionality

## Kafka-Specific Validation

### For Producer Changes
1. Verify events serialize correctly
2. Check delivery callbacks for errors
3. Monitor Kafka UI (http://localhost:8080) for message arrival
4. Confirm correct topic routing

### For Consumer Changes
1. Check offset commit behavior
2. Verify error handling and retries
3. Monitor consumer lag in Kafka UI
4. Validate output format

### For Topic Changes
1. Update `config/kafka_config.py` TOPICS dict
2. Update `scripts/setup_topics.py` if needed
3. Recreate topics: `docker-compose down -v && docker-compose up -d`
4. Re-run: `python scripts/setup_topics.py`

## Git Workflow
1. Create feature branch: `git checkout -b feature/description`
2. Make changes with atomic commits
3. Descriptive commit messages (not "fix", "update")
4. Review with `git diff` before staging

## Documentation Updates
- Update README.md if workflow changes
- Add docstrings for new public methods
- Update event schemas documentation if events change

## Pre-Commit Quality Gate
✅ Black formatting applied  
✅ Ruff linting passed  
✅ Mypy type checking passed  
✅ Tests pass (when available)  
✅ Kafka components manually tested  
✅ Documentation updated  
✅ Git diff reviewed
