from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, Update
from typing import Union


def startswith(text: Union[list[str], str], case_sensitive: bool = False, split_value: str = ' ') -> filters.Filter:
    """Filter startswith. this filter has same behavior as :meth:`~pyrogram.filters.command` but more advanced.

    Args:
        text (Union[list[str], str]):
            The text or list of texts as string the filter should look for
            Examples: "hello", ["hello", "hi", "hallo"]. When a message text containing
            a text arrives, the text itself and its arguments will be stored in the *command*
            field of the :obj:`~pyrogram.types.Message`.

        case_sensitive (bool, optional):
            Pass True if you want your text(s) to be case sensitive. Defaults to Tr.
            Examples: when True, text="Hello" would trigger "Hello" but not "hello".

        split_value (str, optional):
            split the result with the . Defaults to ' '.
            Examples: when you use :meth:`~pyrogram.filters.command` its arguments splited by ' '
            You can customize the split_value now.
    """
    
    async def func(flt, _, update: Message | CallbackQuery) -> bool:
        if isinstance(update, Message):
            data = update.text or update.caption
        elif isinstance(update, CallbackQuery):
            data = update.data
        elif isinstance(update, InlineQuery):
            data = update.query
        else:
            raise ValueError(f"startswith filter doesn't work with {type(update)}")

        if not data:
            return False
        
        if not flt.case_sensitive:
            data = data.lower()

        for txt in flt.text:
            if data.startswith(txt):
                update.command = data.split(flt.split_value)
                return True

        return False

    text = text if isinstance(text, list) else [text]
    text = {t if case_sensitive else t.lower() for t in text}

    return filters.create(func, text=text, split_value=split_value, case_sensitive=case_sensitive)


def endswith(text: Union[list[str], str], case_sensitive: bool = False, split_value: str = ' ') -> filters.Filter:
    """Filter endswith. this filter looking for text(s) you passed in the end of new Update

    Args:
        text (Union[list[str], str]):
            The text or list of texts as string the filter should look for
            Examples: "hello", ["hello", "hi", "hallo"]. When a message text containing
            a text arrives, the text itself and its arguments will be stored in the *command*
            field of the :obj:`~pyrogram.types.Message`.

        case_sensitive (bool, optional):
            Pass True if you want your text(s) to be case sensitive. Defaults to Tr.
            Examples: when True, text="Hello" would trigger "Hello" but not "hello".

        split_value (str, optional):
            split the result with the . Defaults to ' '.
            Examples: when you use :meth:`~pyrogram.filters.command` its arguments splited by ' '
            You can customize the split_value now.
    """
    
    async def func(flt, _, update: Message | CallbackQuery) -> bool:
        if isinstance(update, Message):
            data = update.text or update.caption
        elif isinstance(update, CallbackQuery):
            data = update.data
        elif isinstance(update, InlineQuery):
            data = update.query
        else:
            raise ValueError(f"endswith filter doesn't work with {type(update)}")

        if not data:
            return False
        
        if not flt.case_sensitive:
            data = data.lower()

        for txt in flt.text:
            if data.endswith(txt):
                update.command = data.split(flt.split_value)
                return True

        return False

    text = text if isinstance(text, list) else [text]
    text = {t if case_sensitive else t.lower() for t in text}


    return filters.create(func, text=text, split_value=split_value, case_sensitive=case_sensitive)


def equals(text: Union[list[str], str], prefixes: Union[list[str], str] = '', case_sensitive: bool = False) -> filters.Filter:
    """Filter update equals to, i.e.: text messages are exactly equal to "hello" or "hi" or not?

    Parameters:
        text (``str`` | ``list``):
            The text or list of text as string the filter should look for.
            Examples: "start", ["start", "help", "settings"]. When a message text exactly equal
            a text arrives, the text itself and its arguments will be stored in the *command*
            field of the :obj:`~pyrogram.types.Message`.

        prefixes (``str`` | ``list``, *optional*):
            A prefix or a list of prefixes as string the filter should look for.
            Defaults to "" (no prefix). Examples: ".", "!", ["/", "!", "."], list(".:!").
            Pass "" (empty string) to allow text with no prefix at all.

        case_sensitive (``bool``, *optional*):
            Pass True if you want your text(s) to be case sensitive. Defaults to False.
            Examples: when True, text="Hello" would trigger Hello but not hello.
    """
    
    async def func(flt, _, update: Message | CallbackQuery) -> bool:
        if isinstance(update, Message):
            data = update.text or update.caption
        elif isinstance(update, CallbackQuery):
            data = update.data
        elif isinstance(update, InlineQuery):
            data = update.query
        else:
            raise ValueError(f"equals filter doesn't work with {type(update)}")
        
        if data is None:
            return False

        for prefix in flt.prefixes:
            if not data.startswith(prefix):
                continue

            without_prefix = data[len(prefix):]
            if not flt.case_sensitive:
                without_prefix = without_prefix.lower()

            for txt in flt.text:
                if txt == without_prefix:
                    return True

        return False

    text = text if isinstance(text, list) else [text]
    text = {t if case_sensitive else t.lower() for t in text}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return filters.create(func, text=text, prefixes=prefixes, case_sensitive=case_sensitive)

