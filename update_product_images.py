#!/usr/bin/env python
"""
Helper script to update product images with Supabase Storage URLs.

Usage:
    python update_product_images.py

This script maps product names to image URLs and updates the database.
Requires: Django settings configured
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oliveoshoppe.settings')
django.setup()

from api.models import Plant

# Supabase Storage base URL
SUPABASE_BASE = "https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants"

# Product to image URL mapping
PRODUCT_IMAGES = {
    'Moon Cactus': f'{SUPABASE_BASE}/moon_cactus.jpg',
    'Poinsettia (Christmas Flower)': f'{SUPABASE_BASE}/pintado.jpg',
    'Doña Aurora': f'{SUPABASE_BASE}/donya_aurora.jpg',
    'Citronella (Anti-Mosquito Plant)': f'{SUPABASE_BASE}/citronella.jpg',
    'Crepe Jasmine (Dwarf Pandakaki)': f'{SUPABASE_BASE}/pinwheel.jpg',
    'Sineguelas': f'{SUPABASE_BASE}/sineguelas.jpg',
    'Bermuda Grass (Sod of Grass)': f'{SUPABASE_BASE}/bermudagrass.jpg',
    'Boxwood (Buxus)': f'{SUPABASE_BASE}/buxus.jpg',
    'Bougainvillea': f'{SUPABASE_BASE}/bougainvillea.jpg',
    'Golden Miagos': f'{SUPABASE_BASE}/miagos.jpg',
    'Fukien Tea Tree': f'{SUPABASE_BASE}/fukientea.jpg',
    'Pink Rose (Gertrude Jekyll)': f'{SUPABASE_BASE}/pinkrose.jpg',
    'Chrysanthemum (Mums)': f'{SUPABASE_BASE}/mum1.jpg',
    'Longan Tree': f'{SUPABASE_BASE}/longgan.jpg',
    'American Lemon': f'{SUPABASE_BASE}/americanlemon.jpg',
    'Atsuet': f'{SUPABASE_BASE}/atsuet.jpg',
    'Avocado': f'{SUPABASE_BASE}/avocado.jpg',
    'Banana (Saba)': f'{SUPABASE_BASE}/sagingsaba.jpg',
    'Calamansi': f'{SUPABASE_BASE}/calamansi.jpg',
    'Coffee': f'{SUPABASE_BASE}/coffee.jpg',
    'Mangosteen': f'{SUPABASE_BASE}/mangosteen.jpg',
    'Sunflower': f'{SUPABASE_BASE}/sunflower.jpg',
}

def update_product_images():
    """Update all products with Supabase Storage image URLs."""
    updated = 0
    not_found = []
    
    for product_name, image_url in PRODUCT_IMAGES.items():
        try:
            plant = Plant.objects.get(name=product_name)
            plant.image = image_url
            plant.save()
            print(f'✓ Updated: {product_name}')
            updated += 1
        except Plant.DoesNotExist:
            print(f'✗ Not found: {product_name}')
            not_found.append(product_name)
    
    print(f'\n✓ Updated {updated} products')
    if not_found:
        print(f'✗ {len(not_found)} products not found: {not_found}')
    
    return updated, not_found

if __name__ == '__main__':
    print('=== Updating Product Images with Supabase Storage URLs ===\n')
    update_product_images()
    print('\nDone! All products updated.')
