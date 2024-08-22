from aiohttp import web
import json
import datetime
from models import Base, engine, Ads, Session
from sqlalchemy.exc import IntegrityError

app = web.Application()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def orm_context(app: web.Application):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(error_cls, error_description):
    return error_cls(
        text=json.dumps({"error": error_description}), content_type="application/json"
    )


async def get_ad(ad_id: int, session: Session):
    ad = await session.get(Ads, ad_id)
    if ad is None:
        raise get_error(web.HTTPFound, 'ad not found')
    return ad


async def add_ad(ad: Ads, session: Session):
    session.add(ad)
    await session.commit()
    return ad


class AdsView(web.View):

    @property
    def session(self):
        return self.request.session

    @property
    def ad_id(self):
        return int(self.request.match_info["ad_id"])

    async def get(self):
        ad = await get_ad(self.ad_id, self.session)
        return web.json_response(ad.json)

    async def post(self):
        json_data = await self.request.json()

        ad = Ads(**json_data)
        ad = await add_ad(ad, self.session)
        return web.json_response({"id": ad.id,
                                  "title": ad.title,
                                  "description": ad.description,
                                  "created_at": str(ad.created_at),
                                  "owner": ad.owner,
                                  })

    async def patch(self):
        json_data = await self.request.json()

        ad = await get_ad(self.ad_id, self.session)
        for field, value in json_data.items():
            setattr(ad, field, value)
        ad = await add_ad(ad, self.session)
        return web.json_response(ad.json)

    async def delete(self):
        ad = await get_ad(self.ad_id, self.session)
        await self.session.delete(ad)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes([
    web.post('/ad/', AdsView),
    web.get(r'/ad/{ad_id:\d+}/', AdsView),
    web.patch(r'/ad/{ad_id:\d+}/', AdsView),
    web.delete(r'/ad/{ad_id:\d+}/', AdsView)
])

if __name__ == "__main__":
    web.run_app(app)
