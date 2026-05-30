package publisher

import (
	"context"

	"eda-app/events"
)

//encore:service

type Service struct{}

type PublishRequest struct {
	Message string `json:"message"`
}

//encore:api public method=POST path=/publish
func (s *Service) Publish(ctx context.Context, req *PublishRequest) error {
	if req == nil {
		return nil
	}

	return events.Topic.Publish(ctx, events.MessageEvent{Message: req.Message})
}
