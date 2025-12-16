from django.core.management.base import BaseCommand
from api.models import Plant
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Loads plant products from assets folder into database'

    def handle(self, *args, **options):
        products = [
            {
                'name': 'Moon Cactus',
                'description': 'A small, colorful grafted cactus commonly used as a decorative indoor plant. Place in bright, indirect sunlight; water only when soil is dry.',
                'price': 200.00,
                'stock': 50,
                'image': 'plants/moon_cactus.jpg'
            },
            {
                'name': 'Poinsettia (Christmas Flower)',
                'description': 'A popular ornamental plant known for its red bracts during Christmas season. Keep in bright indirect light; water moderately. Prune after flowering.',
                'price': 300.00,
                'stock': 40,
                'image': 'plants/pintado.jpg'
            },
            {
                'name': 'Doña Aurora',
                'description': 'A Philippine ornamental shrub with large creamy-white bracts. Water regularly and expose to full sun. Regular pruning required.',
                'price': 450.00,
                'stock': 30,
                'image': 'plants/donya_aurora.jpg'
            },
            {
                'name': 'Citronella (Anti-Mosquito Plant)',
                'description': 'Aromatic plant used to repel mosquitoes. Grow in full sun with frequent watering. Trim leaves regularly.',
                'price': 250.00,
                'stock': 60,
                'image': 'plants/citronella.jpg'
            },
            {
                'name': 'Crepe Jasmine (Dwarf Pandakaki)',
                'description': 'A small flowering shrub with fragrant white flowers. Full sun to partial shade; water regularly. Pruning encourages blooms.',
                'price': 300.00,
                'stock': 35,
                'image': 'plants/pinwheel.jpg'
            },
            {
                'name': 'Sineguelas',
                'description': 'A tropical fruit tree producing small sour-sweet fruits. Plant in open area with full sun. Seasonal pruning.',
                'price': 600.00,
                'stock': 20,
                'image': 'plants/sineguelas.jpg'
            },
            {
                'name': 'Bermuda Grass (Sod of Grass)',
                'description': 'Fast-growing lawn grass commonly used for landscaping. Full sun with frequent watering. Regular mowing required.',
                'price': 150.00,
                'stock': 100,
                'image': 'plants/bermudagrass.jpg'
            },
            {
                'name': 'Boxwood (Buxus)',
                'description': 'A low-growing plant used as ground cover and for landscaping. Grow in full sun to partial shade and water regularly.',
                'price': 150.00,
                'stock': 80,
                'image': 'plants/buxus.jpg'
            },
            {
                'name': 'Bougainvillea',
                'description': 'A vibrant flowering plant known for its colorful bracts. Full sun with minimal watering. Pruning controls growth.',
                'price': 350.00,
                'stock': 45,
                'image': 'plants/bougainvillea.jpg'
            },
            {
                'name': 'Golden Miagos',
                'description': 'An ornamental foliage plant with narrow leaves edged in golden yellow. Grow in partial shade to full sun; water regularly.',
                'price': 500.00,
                'stock': 25,
                'image': 'plants/miagos.jpg'
            },
            {
                'name': 'Fukien Tea Tree',
                'description': 'A popular bonsai plant with small glossy leaves. Bright light; water when soil is slightly dry. Regular pruning.',
                'price': 550.00,
                'stock': 15,
                'image': 'plants/fukientea.jpg'
            },
            {
                'name': 'Pink Rose (Gertrude Jekyll)',
                'description': 'An English rose known for its deep pink fragrant flowers. Full sun with frequent watering. Prune after blooming.',
                'price': 450.00,
                'stock': 30,
                'image': 'plants/pinkrose.jpg'
            },
            {
                'name': 'Chrysanthemum (Mums)',
                'description': 'Popular ornamental flowers used for decorations and gifts. Bright light; water regularly. Remove dead flowers.',
                'price': 250.00,
                'stock': 55,
                'image': 'plants/mum1.jpg'
            },
            {
                'name': 'Longan Tree',
                'description': 'Tropical fruit tree producing sweet longan fruits. Full sun; deep watering. Seasonal pruning.',
                'price': 800.00,
                'stock': 10,
                'image': 'plants/longgan.jpg'
            },
            {
                'name': 'American Lemon',
                'description': 'Citrus tree producing sour yellow lemons. Full sun; regular watering. Prune to shape.',
                'price': 700.00,
                'stock': 12,
                'image': 'plants/americanlemon.jpg'
            },
            {
                'name': 'Atsuet',
                'description': 'A small shrub known for its aromatic leaves and medicinal use. Full sun; water moderately. Low maintenance.',
                'price': 350.00,
                'stock': 40,
                'image': 'plants/atsuet.jpg'
            },
            {
                'name': 'Avocado',
                'description': 'A fruit tree producing creamy, nutritious avocados. Full sun; deep watering. Occasional pruning.',
                'price': 750.00,
                'stock': 15,
                'image': 'plants/avocado.jpg'
            },
            {
                'name': 'Banana (Saba)',
                'description': 'A cooking banana variety widely used in Filipino dishes. Full sun; frequent watering. Remove old shoots.',
                'price': 500.00,
                'stock': 25,
                'image': 'plants/sagingsaba.jpg'
            },
            {
                'name': 'Calamansi',
                'description': 'A small citrus tree widely used in Filipino cuisine. Full sun; regular watering. Pruning improves yield.',
                'price': 600.00,
                'stock': 20,
                'image': 'plants/calamansi.jpg'
            },
            {
                'name': 'Coffee',
                'description': 'A tropical plant grown for coffee beans. Partial shade; consistent watering. Regular pruning.',
                'price': 450.00,
                'stock': 30,
                'image': 'plants/coffee.jpg'
            },
            {
                'name': 'Mangosteen',
                'description': 'A slow-growing tropical fruit tree producing sweet purple fruits. Full sun; high humidity. Minimal maintenance once established.',
                'price': 900.00,
                'stock': 8,
                'image': 'plants/mangosteen.jpg'
            },
            {
                'name': 'Sunflower',
                'description': 'A fast-growing flowering plant known for its large yellow blooms. Plant in full sun and water regularly. Remove dried flowers.',
                'price': 250.00,
                'stock': 70,
                'image': 'plants/sunflower.jpg'
            },
        ]

        created = 0
        updated = 0

        for product_data in products:
            plant, created_new = Plant.objects.update_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'image': product_data['image']
                }
            )
            if created_new:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {plant.name}'))
            else:
                updated += 1
                self.stdout.write(self.style.WARNING(f'! Updated: {plant.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Products loaded: {created} created, {updated} updated'
        ))

            {
                'name': 'Poinsettia',
                'scientific_name': 'Euphorbia pulcherrima',
                'tagalog_name': 'Pintado / Christmas Flower',
                'description': 'A popular ornamental plant known for its red bracts during Christmas season.',
                'care_instructions': 'Keep in bright indirect light; water moderately. Prune after flowering.',
                'light': 'Bright indirect',
                'water': 'Moderate',
                'soil': 'Well-drained soil',
                'temperature': '18–26°C',
                'plant_type': 'Flowering Plant',
                'price': 300.00,
                'stock': 40,
                'image': 'plants/pintado.jpg'
            },
            {
                'name': 'Doña Aurora',
                'scientific_name': "Mussaenda philippica 'Doña Aurora'",
                'tagalog_name': 'Doña Aurora',
                'description': 'A Philippine ornamental shrub with large creamy-white bracts.',
                'care_instructions': 'Water regularly and expose to full sun. Regular pruning.',
                'light': 'Full sun',
                'water': 'Regular',
                'soil': 'Loamy soil',
                'temperature': 'Tropical',
                'plant_type': 'Shrub / Flowering Plant',
                'price': 450.00,
                'stock': 30,
                'image': 'plants/donya_aurora.jpg'
            },
            {
                'name': 'Citronella',
                'scientific_name': 'Cymbopogon nardus',
                'tagalog_name': 'Tanglad',
                'description': 'Aromatic plant used to repel mosquitoes.',
                'care_instructions': 'Grow in full sun with frequent watering. Trim leaves regularly.',
                'light': 'Full sun',
                'water': 'Moderate to high',
                'soil': 'Well-drained soil',
                'temperature': 'Tropical',
                'plant_type': 'Grass',
                'price': 250.00,
                'stock': 60,
                'image': 'plants/citronella.jpg'
            },
            {
                'name': 'Crepe Jasmine',
                'scientific_name': 'Tabernaemontana divaricata',
                'tagalog_name': 'Pandakaki',
                'description': 'A small flowering shrub with fragrant white flowers.',
                'care_instructions': 'Full sun to partial shade; water regularly. Pruning encourages blooms.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Fertile soil',
                'temperature': 'Warm',
                'plant_type': 'Shrub / Flowering Plant',
                'price': 300.00,
                'stock': 35,
                'image': 'plants/pinwheel.jpg'
            },
            {
                'name': 'Sineguelas',
                'scientific_name': 'Spondias purpurea',
                'tagalog_name': 'Sineguelas',
                'description': 'A tropical fruit tree producing small sour-sweet fruits.',
                'care_instructions': 'Plant in open area with full sun. Seasonal pruning.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Well-drained soil',
                'temperature': 'Tropical',
                'plant_type': 'Tree',
                'price': 600.00,
                'stock': 20,
                'image': 'plants/sineguelas.jpg'
            },
            {
                'name': 'Bermuda Grass',
                'scientific_name': 'Cynodon dactylon',
                'tagalog_name': 'Bermuda grass',
                'description': 'Fast-growing lawn grass commonly used for landscaping.',
                'care_instructions': 'Full sun with frequent watering. Regular mowing.',
                'light': 'Full sun',
                'water': 'High',
                'soil': 'Sandy loam',
                'temperature': 'Warm',
                'plant_type': 'Grass',
                'price': 150.00,
                'stock': 100,
                'image': 'plants/bermudagrass.jpg'
            },
            {
                'name': 'Boxwood',
                'scientific_name': 'Buxus spp.',
                'tagalog_name': 'Buxus grass',
                'description': 'A low-growing, grass-like plant used as ground cover and for landscaping.',
                'care_instructions': 'Grow in full sun to partial shade and water regularly. Requires trimming.',
                'light': 'Full sun to partial shade',
                'water': 'Moderate to high',
                'soil': 'Well-drained soil',
                'temperature': 'Warm',
                'plant_type': 'Grass',
                'price': 150.00,
                'stock': 80,
                'image': 'plants/buxus.jpg'
            },
            {
                'name': 'Bougainvillea',
                'scientific_name': 'Bougainvillea spp.',
                'tagalog_name': 'Bougainvillea',
                'description': 'A vibrant flowering plant known for its colorful bracts.',
                'care_instructions': 'Full sun with minimal watering. Pruning controls growth.',
                'light': 'Full sun',
                'water': 'Low',
                'soil': 'Well-drained',
                'temperature': 'Warm',
                'plant_type': 'Flowering Plant / Shrub',
                'price': 350.00,
                'stock': 45,
                'image': 'plants/bougainvillea.jpg'
            },
            {
                'name': 'Golden Miagos',
                'scientific_name': "Osmoxylon lineare 'Golden'",
                'tagalog_name': 'Golden Miagos',
                'description': 'An ornamental foliage plant with narrow leaves edged in golden yellow.',
                'care_instructions': 'Grow in partial shade to full sun; water regularly. Low maintenance.',
                'light': 'Partial shade to full sun',
                'water': 'Moderate',
                'soil': 'Well-drained, fertile soil',
                'temperature': 'Tropical',
                'plant_type': 'Shrub / Ornamental Plant',
                'price': 500.00,
                'stock': 25,
                'image': 'plants/miagos.jpg'
            },
            {
                'name': 'Fukien Tea Tree',
                'scientific_name': 'Carmona retusa',
                'tagalog_name': 'Tsaang Gubat',
                'description': 'A popular bonsai plant with small glossy leaves.',
                'care_instructions': 'Bright light; water when soil is slightly dry. Regular pruning.',
                'light': 'Bright indirect',
                'water': 'Moderate',
                'soil': 'Well-drained',
                'temperature': 'Warm',
                'plant_type': 'Tree / Shrub',
                'price': 550.00,
                'stock': 15,
                'image': 'plants/fukientea.jpg'
            },
            {
                'name': 'Pink Rose (Gertrude Jekyll)',
                'scientific_name': "Rosa 'Gertrude Jekyll'",
                'tagalog_name': 'Rosas',
                'description': 'An English rose known for its deep pink fragrant flowers.',
                'care_instructions': 'Full sun with frequent watering. Prune after blooming.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Fertile soil',
                'temperature': 'Cool to warm',
                'plant_type': 'Flowering Plant / Shrub',
                'price': 450.00,
                'stock': 30,
                'image': 'plants/pinkrose.jpg'
            },
            {
                'name': 'Chrysanthemum',
                'scientific_name': 'Chrysanthemum spp.',
                'tagalog_name': 'Mums',
                'description': 'Popular ornamental flowers used for decorations and gifts.',
                'care_instructions': 'Bright light; water regularly. Remove dead flowers.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Well-drained',
                'temperature': 'Cool to warm',
                'plant_type': 'Flowering Plant',
                'price': 250.00,
                'stock': 55,
                'image': 'plants/mum1.jpg'
            },
            {
                'name': 'Longan Tree',
                'scientific_name': 'Dimocarpus longan',
                'tagalog_name': 'Longan',
                'description': 'Tropical fruit tree producing sweet longan fruits.',
                'care_instructions': 'Full sun; deep watering. Seasonal pruning.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Well-drained',
                'temperature': 'Tropical',
                'plant_type': 'Tree',
                'price': 800.00,
                'stock': 10,
                'image': 'plants/longan.jpg'
            },
            {
                'name': 'American Lemon',
                'scientific_name': 'Citrus limon',
                'tagalog_name': 'Lemon',
                'description': 'Citrus tree producing sour yellow lemons.',
                'care_instructions': 'Full sun; regular watering. Prune to shape.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Sandy loam',
                'temperature': 'Warm',
                'plant_type': 'Tree',
                'price': 700.00,
                'stock': 12,
                'image': 'plants/americanlemon.jpg'
            },
            {
                'name': 'Atsuet',
                'scientific_name': 'Bixa orellana',
                'tagalog_name': 'Atsuet',
                'description': 'A small shrub known for its aromatic leaves and medicinal use.',
                'care_instructions': 'Full sun; water moderately. Low maintenance.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Well-drained',
                'temperature': 'Tropical',
                'plant_type': 'Shrub',
                'price': 350.00,
                'stock': 40,
                'image': 'plants/atsuet.jpg'
            },
            {
                'name': 'Avocado',
                'scientific_name': 'Persea americana',
                'tagalog_name': 'Abukado',
                'description': 'A fruit tree producing creamy, nutritious avocados.',
                'care_instructions': 'Full sun; deep watering. Occasional pruning.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Well-drained',
                'temperature': 'Warm',
                'plant_type': 'Tree',
                'price': 750.00,
                'stock': 15,
                'image': 'plants/avocado.jpg'
            },
            {
                'name': 'Banana (Saba)',
                'scientific_name': 'Musa spp.',
                'tagalog_name': 'Saging na Saba',
                'description': 'A cooking banana variety widely used in Filipino dishes.',
                'care_instructions': 'Full sun; frequent watering. Remove old shoots.',
                'light': 'Full sun',
                'water': 'High',
                'soil': 'Rich soil',
                'temperature': 'Tropical',
                'plant_type': 'Herb',
                'price': 500.00,
                'stock': 25,
                'image': 'plants/sagingsaba.jpg'
            },
            {
                'name': 'Calamansi',
                'scientific_name': 'Citrus microcarpa',
                'tagalog_name': 'Calamansi',
                'description': 'A small citrus tree widely used in Filipino cuisine.',
                'care_instructions': 'Full sun; regular watering. Pruning improves yield.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Well-drained',
                'temperature': 'Warm',
                'plant_type': 'Tree',
                'price': 600.00,
                'stock': 20,
                'image': 'plants/calamansi.jpg'
            },
            {
                'name': 'Coffee',
                'scientific_name': 'Coffea arabica',
                'tagalog_name': 'Kape',
                'description': 'A tropical plant grown for coffee beans.',
                'care_instructions': 'Partial shade; consistent watering. Regular pruning.',
                'light': 'Partial shade',
                'water': 'Moderate',
                'soil': 'Rich soil',
                'temperature': 'Cool to warm',
                'plant_type': 'Shrub',
                'price': 450.00,
                'stock': 30,
                'image': 'plants/coffee.jpg'
            },
            {
                'name': 'Mangosteen',
                'scientific_name': 'Garcinia mangostana',
                'tagalog_name': 'Mangostan',
                'description': 'A slow-growing tropical fruit tree producing sweet purple fruits.',
                'care_instructions': 'Full sun; high humidity. Minimal maintenance once established.',
                'light': 'Full sun',
                'water': 'High',
                'soil': 'Rich, well-drained',
                'temperature': 'Tropical',
                'plant_type': 'Tree',
                'price': 900.00,
                'stock': 8,
                'image': 'plants/mangosteen.jpg'
            },
            {
                'name': 'Sunflower',
                'scientific_name': 'Helianthus annuus',
                'tagalog_name': 'Mirasol',
                'description': 'A fast-growing flowering plant known for its large yellow blooms.',
                'care_instructions': 'Plant in full sun and water regularly. Remove dried flowers.',
                'light': 'Full sun',
                'water': 'Moderate',
                'soil': 'Well-drained, fertile soil',
                'temperature': 'Warm (20–30°C)',
                'plant_type': 'Flowering Plant',
                'price': 250.00,
                'stock': 70,
                'image': 'plants/sunflower.jpg'
            },
        ]

        created = 0
        updated = 0

        for product_data in products:
            plant, created_new = Plant.objects.update_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created_new:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {plant.name}'))
            else:
                updated += 1
                self.stdout.write(self.style.WARNING(f'! Updated: {plant.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Products loaded: {created} created, {updated} updated'
        ))
