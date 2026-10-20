-- Loads the Earth2Road planet extension; it stays idle outside the level e2r_world.
-- The unload mode must be registered before the load, otherwise core_modmanager warns at startup.
setExtensionUnloadMode('e2r_world', 'manual')
extensions.load('e2r_world')
