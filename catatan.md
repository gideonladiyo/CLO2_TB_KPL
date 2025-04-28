## Endpoint yang Bisa Dibuat
| Endpoint | Method | Deskripsi | Peran |
|:---|:---|:---|:---|
| `/items` | GET | List semua barang yang tersedia | User |
| `/items/{item_id}` | GET | Detail 1 barang | User |
| `/orders` | POST | Membuat pesanan baru (pilih barang & jumlah) | User |
| `/orders` | GET | List semua pesanan | Admin/User (depending auth) |
| `/orders/{order_id}` | GET | Detail pesanan tertentu | User |
| `/orders/{order_id}/pay` | POST | Simulasi pembayaran pesanan | User |
| `/orders/{order_id}/cancel` | POST | Membatalkan pesanan (kalau masih dalam status tertentu) | User |
| `/orders/{order_id}/ship` | POST | Admin memproses pengiriman | Admin |
| `/orders/{order_id}/complete` | POST | Tandai pesanan selesai (barang diterima) | User |
| `/orders/{order_id}/status` | PATCH | Update manual status pesanan (pakai FSM validasi) | Admin |
| `/orders/stats` | GET | Statistik pesanan: berapa pending, shipped, completed, canceled | Admin |