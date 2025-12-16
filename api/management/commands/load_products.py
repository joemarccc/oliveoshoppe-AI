from django.core.management.base import BaseCommand
from api.models import Plant


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
