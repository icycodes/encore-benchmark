package subscriber

import (
	"context"

	"eda-app/events"
	"encore.dev/storage/sqldb"
)

//encore:service

type Service struct{}

var MessagesDB = sqldb.NewDatabase("messages", sqldb.DatabaseConfig{
	Migrations: "migrations",
})

type Message struct {
	Message string `json:"message"`
}

type ListResponse struct {
	Messages []Message `json:"messages"`
}

//encore:api public method=GET path=/messages
func (s *Service) ListMessages(ctx context.Context) (*ListResponse, error) {
	rows, err := MessagesDB.Query(ctx, "SELECT message FROM messages ORDER BY id")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	messages := make([]Message, 0)
	for rows.Next() {
		var message string
		if err := rows.Scan(&message); err != nil {
			return nil, err
		}
		messages = append(messages, Message{Message: message})
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}

	return &ListResponse{Messages: messages}, nil
}

//encore:subscribes topic=events.Topic
func (s *Service) HandleMessage(ctx context.Context, msg *events.MessageEvent) error {
	_, err := MessagesDB.Exec(ctx, "INSERT INTO messages (message) VALUES ($1)", msg.Message)
	return err
}
