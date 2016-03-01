"""
Core logic for Comprehensive Theming.
"""
from path import Path

from django.conf import settings


def comprehensive_theme_changes(theme_dir):
    """
    Calculate the set of changes needed to enable a comprehensive theme.

    Arguments:
        theme_dir (path.path): the full path to the theming directory to use.

    Returns:
        A dict indicating the changes to make:

            * 'settings': a dictionary of settings names and their new values.

            * 'template_paths': a list of directories to prepend to template
                lookup path.

    """

    changes = {
        'settings': {},
        'template_paths': [],
    }
    root = Path(settings.PROJECT_ROOT)
    if root.name == "":
        root = root.parent

    component_dir = theme_dir / root.name

    templates_dir = component_dir / "templates"
    if templates_dir.isdir():
        changes['template_paths'].append(templates_dir)

    staticfiles_dir = component_dir / "static"
    if staticfiles_dir.isdir():
        changes['settings']['STATICFILES_DIRS'] = [staticfiles_dir] + settings.STATICFILES_DIRS

    locale_dir = component_dir / "conf" / "locale"
    if locale_dir.isdir():
        changes['settings']['LOCALE_PATHS'] = [locale_dir] + settings.LOCALE_PATHS

    return changes


def enable_comprehensive_theme(theme_dir):
    """
    Add directories to relevant paths for comprehensive theming.
    """
    changes = comprehensive_theme_changes(theme_dir)

    # Use the changes
    for name, value in changes['settings'].iteritems():
        setattr(settings, name, value)
    for template_dir in changes['template_paths']:
        settings.DEFAULT_TEMPLATE_ENGINE['DIRS'].insert(0, template_dir)
        settings.MAKO_TEMPLATES['main'].insert(0, template_dir)
