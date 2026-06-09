
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('category/', include('category.urls', namespace='category')),
    path('item/', include('item.urls', namespace='item')),
    path('contactchannel/', include('contactchannel.urls', namespace='contactchannel')),
    path('user/', include('user.urls', namespace='user')),
    path('auction/', include('auction.urls', namespace='auction')),
    path('auctionitem/', include('auctionitem.urls', namespace='auctionitem')),
    path('auctionbid/', include('auctionbid.urls', namespace='auctionbid')),
    path('receiptpayment/', include('receiptpayment.urls', namespace='receiptpayment')),
    path('auctioneer/', include('auctioneer.urls', namespace='auctioneer')),
    path('payment/', include('payment.urls', namespace='payment')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
