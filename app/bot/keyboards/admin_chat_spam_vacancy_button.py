from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from bot.filters.callback.spam_vacancy_callback import (
    IncrementUserBonusForSpamVacancyCallback,
    NotSpamButDeleteMessagesForSpamVacancyCallback,
    RejectSpamVacancyCallback,
    SpamAndIncrementUserBonusForSpamVacancyCallback,
    SpamVacancyCallbackForAdmin,
)
from config import i18n

MAX_COUNT_BUTTON_IN_LINE = 1


def admin_chat_spam_vacancy_button(
    spam_vacancy: SpamVacancyCallbackForAdmin,
    increment_user_bonus_for_spam_vacancy: IncrementUserBonusForSpamVacancyCallback,
    reject_spam_vacancy: RejectSpamVacancyCallback,
    spam_and_increment_user_bonus_for_spam_vacancy: SpamAndIncrementUserBonusForSpamVacancyCallback,
    not_spam_but_delete_messages_for_spam_vacancy: NotSpamButDeleteMessagesForSpamVacancyCallback,
) -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()

    kb.button(
        text=i18n["spam"]["confirm_spam"],
        callback_data=spam_vacancy.pack(),
    )
    kb.button(
        text=i18n["spam"]["increment_user_bonus_for_spam_vacancy"],
        callback_data=increment_user_bonus_for_spam_vacancy.pack(),
    )
    kb.button(
        text=i18n["spam"]["spam_and_increment_user_bonus"],
        callback_data=spam_and_increment_user_bonus_for_spam_vacancy.pack(),
    )
    kb.button(
        text=i18n["spam"]["not_spam_but_delete_messages"],
        callback_data=not_spam_but_delete_messages_for_spam_vacancy.pack(),
    )
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
