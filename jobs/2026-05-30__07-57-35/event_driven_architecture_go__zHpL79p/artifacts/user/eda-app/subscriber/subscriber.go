package subscriber

import (
	"context"

	"eda-app/publisher"

	"encore.dev/pubsub"
	"encore.dev/storage/sqldb"
)

// Subscription subscribes to the publisher's topic.
var Subscription = pubsub.NewSubscription[publisher.MessageEvent]("message-sub", publisher.Topic, pubsub.SubscriptionConfig{
	Handler: handleMessage,
})

// handleMessage processes incoming messages from the Pub/Sub topic.
func handleMessage(ctx context.Context, event *publisher.MessageEvent) error {
	_, err := sqldb.Exec(ctx, "INSERT INTO messages (message) VALUES ($1)", event.Message)
	return err
}

// MessageEntry represents a stored message.
type MessageEntry struct {
	Message string `json:"message"`
}

// MessagesResponse is the response for the GET /messages endpoint.
type MessagesResponse struct {
	Messages []MessageEntry `json:"messages"`
}

// GetMessages returns all stored messages.
//
//encore:api public method=GET path=/messages
func GetMessages(ctx context.Context) (*MessagesResponse, error) {
	rows, err := sqldb.Query(ctx, "SELECT message FROM messages")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	messages := []MessageEntry{}
	for rows.Next() {
		var msg string
		if err := rows.Scan(&msg); err != nil {
			return nil, err
		}
		messages = append(messages, MessageEntry{Message: msg})
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}

	return &MessagesResponse{Messages: messages}, nil
}