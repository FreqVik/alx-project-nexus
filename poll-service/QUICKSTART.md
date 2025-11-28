# Quick Start Guide - Poll Service with RabbitMQ

## 🚀 Getting Started

### Option 1: Using Docker Compose (Recommended)

1. **Start all services:**
```bash
docker-compose up -d
```

This will start:
- RabbitMQ on ports 5672 (AMQP) and 15672 (Management UI)
- Poll Service on port 8000

2. **Access the services:**
- Poll Service API: http://localhost:8000/docs
- RabbitMQ Management UI: http://localhost:15672 (guest/guest)

3. **Test the API:**
```bash
# Create a poll
curl -X POST "http://localhost:8000/polls/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Best Programming Language?",
    "description": "Vote for your favorite",
    "author_id": "user-123",
    "type": "single",
    "status": "draft",
    "allow_anonymous": true,
    "allow_change_vote": false,
    "options": [
      {"text": "Python", "order": 0},
      {"text": "JavaScript", "order": 1},
      {"text": "Go", "order": 2}
    ]
  }'
```

4. **View published events in RabbitMQ:**
- Go to http://localhost:15672
- Login with guest/guest
- Navigate to "Exchanges" → "poll_events"
- You'll see the event has been published!

---

### Option 2: Local Development

1. **Start RabbitMQ:**
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

2. **Install dependencies:**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env if needed
```

4. **Run migrations:**
```bash
alembic upgrade head
```

5. **Start the service:**
```bash
uvicorn main:app --reload --port 8000
```

---

## 🧪 Testing Event Publishing

### Test Event Producer

```bash
python test_events.py
```

This will publish a test event to RabbitMQ.

### Run Event Consumer (Example)

In a separate terminal:

```bash
pip install pika  # If not already installed
python examples/event_consumer.py
```

This will listen for all poll events and print them to the console.

Now create a poll via the API, and you'll see the event appear in the consumer!

---

## 📡 Event Flow Example

1. **Create a poll** (via API)
   ```
   POST /polls/
   ```

2. **Poll Service publishes** `poll.created` event to RabbitMQ

3. **Other services consume** the event:
   - 📊 **vote-service**: Initializes vote tracking
   - 📈 **results-service**: Sets up results aggregation
   - 🔔 **notification-service**: Sends notifications

4. **Update poll status** to "active"
   ```
   PATCH /polls/{id}
   {"status": "active"}
   ```

5. **Poll Service publishes** both:
   - `poll.updated` event
   - `poll.started` event

6. **Services react**:
   - 📊 **vote-service**: Enables voting
   - 🔔 **notification-service**: Notifies users poll is live

---

## 🔍 Monitoring Events

### RabbitMQ Management UI

1. Go to http://localhost:15672
2. Login: guest/guest
3. Check:
   - **Exchanges** → `poll_events` to see the exchange
   - **Queues** to see consumer queues
   - **Connections** to see active connections

### Published Event Types

- `poll.created` - New poll created
- `poll.updated` - Poll metadata updated
- `poll.started` - Poll became active
- `poll.closed` - Poll was closed

---

## 🛠 Development Tips

### Update Requirements

After modifying `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Create New Migration

After modifying models:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### View Logs

Docker Compose:
```bash
docker-compose logs -f poll-service
docker-compose logs -f rabbitmq
```

---

## 🐛 Troubleshooting

### RabbitMQ Connection Failed

**Error:** `Failed to connect to RabbitMQ`

**Solution:**
1. Check RabbitMQ is running: `docker ps | grep rabbitmq`
2. Check connection settings in `.env`
3. Verify RabbitMQ health: `docker logs rabbitmq`

### Events Not Publishing

**Check:**
1. RabbitMQ is running and accessible
2. Exchange `poll_events` exists (check Management UI)
3. Service logs for errors: `docker-compose logs poll-service`

### Consumer Not Receiving Events

**Check:**
1. Queue is bound to exchange with correct routing key
2. Consumer is connected (check RabbitMQ Connections tab)
3. Events are being published (check Exchange tab in RabbitMQ UI)

---

## 📚 Next Steps

- Implement **vote-service** to consume poll events
- Add **results-service** for aggregating votes
- Build **notification-service** for user alerts
- Add authentication and authorization
- Implement poll scheduling with background workers
