from mysite.database.models import UserProfile,Category,Product,SubCategory,Review,RefreshToken,ProductImage
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.user_token]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.category_name]


class SubCategoryAdmin(ModelView, model=SubCategory):
    column_list = [SubCategory.sub_category_name]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.product_name]


class ProductImageAdmin(ModelView, model=ProductImage):
    column_list = [ProductImage.image]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.product_rev]




