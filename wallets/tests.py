from django.test import TestCase

"""
1) проверка создания Wallet
2) проверка полей:
    - уникальное имя
    - modified обновляется
    - автобаланс 3 евро/доллара или 100 рублей
3) проверка 5 кошельков
4) проверка удаления кошелька
"""


# class RecipeTestCase(TestCase):
#     def setUp(self):
#         self.user_a = get_user_model().objects.create_user('qwe', password='qwe')
#         self.recipe_a = Recipe.objects.create(
#             name='Тушеная курица',
#             user=self.user_a,
#             description='Тушим курицу',
#         )
#
#     def test_user_count(self):
#         qs = get_user_model().objects.all()
#         self.assertEqual(qs.count(), 1)
