from service.reviewService import ReviewService


class ReviewController:
    def __init__(self, reviewservice: ReviewService):
        self.review_service = reviewservice
