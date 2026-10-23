"""Checks that the generated Xcode project still deploys back to iOS 15."""
import unittest

from scripts.common import REPO


class DeploymentTargetTests(unittest.TestCase):
    def test_project_and_every_target_deploy_to_ios_15(self):
        configure = (REPO / 'scripts/configure_xcode.rb').read_text(encoding='utf-8')
        # The project and every target carry their own deployment target; one left
        # at a newer version keeps an iOS 15 device from installing the app.
        self.assertEqual(configure.count("'IPHONEOS_DEPLOYMENT_TARGET'"), 2)
        self.assertEqual(configure.count("['IPHONEOS_DEPLOYMENT_TARGET'] = '15.0'"), 2)

    def test_native_code_does_not_need_a_newer_system(self):
        # The HUD command grew in iOS 15; nothing under src may use a newer class
        # or an availability check that would silently raise the floor again.
        sources = list((REPO / 'src/runtime').glob('*.mm')) + list((REPO / 'src/runtime').glob('*.h'))
        self.assertTrue(sources)
        text = '\n'.join(path.read_text(encoding='utf-8') for path in sources)
        for newer in ('UICalendarView', 'UIEditMenuInteraction', 'UIPasteControl',
                      'GCDevicePhysicalInput', 'UIWindowSceneGeometry'):
            self.assertNotIn(newer, text, f'{newer} needs a system newer than iOS 15')
