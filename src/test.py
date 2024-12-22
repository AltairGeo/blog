import db
import asyncio


print(asyncio.run(db.control.UserORM.GetUserAvatarHashById(-1)))