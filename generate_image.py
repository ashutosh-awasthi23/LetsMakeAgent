from PIL import Image, ImageDraw

# Ek white image create karein (400x450 pixels)
img = Image.new('RGB', (400, 450), color='white')
d = ImageDraw.Draw(img)

# Receipt ka realistic text data
receipt_text = """
================================
       FRESH MART GROCERY
================================
Date: 29-Sep-2026
Time: 10:45 AM

Item                     Price
--------------------------------
1x Organic Milk          $4.50
1x Whole Wheat Bread     $3.00
1x Dozen Eggs            $2.50
2x Avocados              $3.00
--------------------------------
Subtotal:               $13.00
Tax (5%):                $0.65
--------------------------------
TOTAL AMOUNT:           $13.65
================================
   Thank You for shopping!
"""

# Text ko image par draw karein
d.text((20, 20), receipt_text, fill='black')

# Image ko save karein
image_path = 'test_bill.jpg'
img.save(image_path)
print(f"Success: '{image_path}' successfully generated!")