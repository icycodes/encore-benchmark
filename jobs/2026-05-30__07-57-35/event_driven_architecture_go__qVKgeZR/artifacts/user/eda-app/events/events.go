package events

import "encore.dev/pubsub"

type MessageEvent struct {
	Message string `json:"message"`
}

var Topic = pubsub.NewTopic[MessageEvent]("messages", pubsub.TopicConfig{})
