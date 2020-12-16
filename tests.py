import os
import re
import time

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from gallery.models import Photo, PhotoSet


class PhotoSetTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_add_photosets(self):
        # cleanup
        PhotoSet.objects.all().delete()

        p1 = PhotoSet.objects.create(title='A Photo Set',
            slug='a-photo-set', meta_description='This is a photo set.')
        p2 = PhotoSet.objects.create(title='Another Photo Set',
            slug='another-photo-set', sort_order=0,
            meta_description='This is a photo set.')

        self.assertEqual(PhotoSet.objects.all().count(), 2)
        self.assertEqual(PhotoSet.objects.all()[0], p2)

        r = self.client.get(reverse('gallery_list'))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'gallery/photoset_list.html')

        r = self.client.get(reverse('gallery_detail',
            kwargs={'slug': p1.slug}))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'gallery/photoset_detail.html')


class PhotoTest(TestCase):

    def setUp(self):
        self.client = Client()

        # cleanup
        Photo.objects.all().delete()
        PhotoSet.objects.all().delete()

        # create a photoset
        PhotoSet.objects.create(title='A Photo Set', slug='a-photo-set',
            meta_description='This is a photo set.')

    def test_add_photo(self):
        photo_name = "test-image-%s" % time.time()
        photo = Photo.objects.create(caption='Image caption.',
            photoset=PhotoSet.objects.all()[0])
        photo.image.save("%s.jpg" % photo_name,
            ContentFile(open(os.path.join(os.path.dirname(__file__),
            '../test_data/test-image.jpg'), 'rb').read()), save=True)

        self.assertEqual(Photo.objects.all().count(), 1)
        self.assertEqual(PhotoSet.objects.all()[0].photo_set.all().count(), 1)
        self.assertEqual(PhotoSet.objects.all()[0].albumcover().url,
            'http://127.0.0.1:8000/media/gallery/%s.jpg' % photo_name)

    def test_description_limited_to_250_chars(self):
        ps = PhotoSet.objects.all()[0]
        ps.meta_description = 'x' * 250
        ps.save()
        self.assertEqual(PhotoSet.objects.all()[0].meta_description,
            'x' * 250)
        ps.meta_description = 'x' * 251
        self.assertRaises(ValidationError, ps.save())

    def tearDown(self):
        # remove all files from the dynamic_media/avatars directory
        folder = os.path.join(os.path.dirname(__file__), '../myproject/media')
        for the_file in os.listdir(folder):
            if re.search('^test-image', the_file):
                file_path = os.path.join(folder, the_file)
                try:
                    os.unlink(file_path)
                except Exception, e:
                    print e
