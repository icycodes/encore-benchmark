package publisher

import (
	"context"

	"encore.dev/pubsub"
)

// MessageEvent is the event published to the topic.
type MessageEvent struct {
	Message string
}

// Topic is the Pub/Sub topic for messages.
var Topic = pubsub.NewTopic[MessageEvent]("message-topic", pubsub.TopicConfig{
	DeliveryRetry: pubsub.AtLeastOnce,
})

// PublishParams is the request body for the publish endpoint.
type PublishParams struct {
	Message string `json:"message"`
}

// Publish publishes a message to the Pub/Sub topic.
//
//encore:api public method=POST path=/publish
func Publish(ctx context.Context, params *PublishParams) error {
	return Topic.Publish(ctx, &MessageEvent{Message: params.Message})
}