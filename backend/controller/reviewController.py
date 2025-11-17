from service.reviewService import ReviewService


class ReviewController:
    def __init__(self, review_service: ReviewService):
        self.review_service = review_service
